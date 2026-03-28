const CONFIG = {
  expectedAccount: 'WORK_ACCOUNT_EMAIL',
  rootFolderName: 'Prumo',
  snapshotsFolderName: 'snapshots',
  snapshotDocumentName: 'email-snapshot',
  defaultLookbackHours: 24,
  searchBatchSize: 100,
  version: '1.0'
};

function runSnapshot(since) {
  const account = resolveAccount_();
  validateExpectedAccount_(account);

  const sinceDate = parseSince_(since);
  const snapshot = {
    version: CONFIG.version,
    account: account || CONFIG.expectedAccount,
    generated_at: toIsoString_(new Date()),
    since: toIsoString_(sinceDate),
    emails: [],
    calendar: {
      today: [],
      tomorrow: []
    }
  };

  try {
    snapshot.emails = loadEmails_(sinceDate, snapshot.account);
  } catch (error) {
    snapshot.emails_error = formatError_(error);
    logError_('Gmail snapshot failed', error);
  }

  try {
    snapshot.calendar = loadCalendar_();
  } catch (error) {
    snapshot.calendar = { today: [], tomorrow: [] };
    snapshot.calendar_error = formatError_(error);
    logError_('Calendar snapshot failed', error);
  }

  const file = saveSnapshotToDrive_(snapshot);

  return {
    ok: !snapshot.emails_error && !snapshot.calendar_error,
    document_id: file.getId(),
    document_name: file.getName(),
    account: snapshot.account,
    generated_at: snapshot.generated_at
  };
}

function installOrRefreshTrigger() {
  removeTriggersForHandler_('runSnapshot');

  ScriptApp.newTrigger('runSnapshot')
    .timeBased()
    .everyMinutes(15)
    .create();
}

function removeSnapshotTriggers() {
  removeTriggersForHandler_('runSnapshot');
}

function loadEmails_(sinceDate, account) {
  const queryDate = Utilities.formatDate(
    sinceDate,
    Session.getScriptTimeZone(),
    'yyyy/MM/dd'
  );
  const query = 'in:anywhere after:' + queryDate + ' -in:drafts';
  const selfAddresses = buildSelfAddressSet_(account);
  const emailsById = {};
  let start = 0;

  while (true) {
    const threads = GmailApp.search(query, start, CONFIG.searchBatchSize);

    if (!threads.length) {
      break;
    }

    for (let i = 0; i < threads.length; i += 1) {
      const messages = threads[i].getMessages();

      for (let j = 0; j < messages.length; j += 1) {
        const message = messages[j];

        if (message.isDraft()) {
          continue;
        }

        if (message.getDate().getTime() < sinceDate.getTime()) {
          continue;
        }

        if (!isIncomingMessage_(message, selfAddresses)) {
          continue;
        }

        emailsById[message.getId()] = buildEmailSnapshot_(message);
      }
    }

    start += threads.length;

    if (threads.length < CONFIG.searchBatchSize) {
      break;
    }
  }

  return Object.keys(emailsById)
    .map(function mapEmail(id) {
      return emailsById[id];
    })
    .sort(function sortByNewest(a, b) {
      return new Date(b.date).getTime() - new Date(a.date).getTime();
    });
}

function loadCalendar_() {
  const calendar = CalendarApp.getDefaultCalendar();
  const today = new Date();
  const tomorrow = new Date(today.getTime());

  tomorrow.setDate(tomorrow.getDate() + 1);

  return {
    today: buildEventSnapshots_(calendar.getEventsForDay(today)),
    tomorrow: buildEventSnapshots_(calendar.getEventsForDay(tomorrow))
  };
}

function buildEventSnapshots_(events) {
  return events
    .map(function mapEvent(event) {
      return {
        title: event.getTitle(),
        start: toIsoString_(event.getStartTime()),
        end: toIsoString_(event.getEndTime()),
        location: resolveEventLocation_(event),
        attendees_count: getAttendeesCount_(event)
      };
    })
    .sort(function sortByStart(a, b) {
      return new Date(a.start).getTime() - new Date(b.start).getTime();
    });
}

function buildEmailSnapshot_(message) {
  const plainBody = safeGetPlainBody_(message);
  const labels = message.getThread().getLabels().map(function mapLabel(label) {
    return label.getName();
  });

  return {
    id: message.getId(),
    from: message.getFrom(),
    subject: message.getSubject(),
    date: toIsoString_(message.getDate()),
    snippet: buildSnippet_(plainBody),
    labels: labels,
    has_attachments: message.getAttachments({
      includeAttachments: true,
      includeInlineImages: false
    }).length > 0
  };
}

function saveSnapshotToDrive_(snapshot) {
  const rootFolder = DriveApp.getRootFolder();
  const prumoFolder = findOrCreateFolder_(rootFolder, CONFIG.rootFolderName);
  const snapshotsFolder = findOrCreateFolder_(prumoFolder, CONFIG.snapshotsFolderName);
  const content = JSON.stringify(snapshot, null, 2);
  const existingFiles = snapshotsFolder.getFilesByName(CONFIG.snapshotDocumentName);

  if (existingFiles.hasNext()) {
    const file = existingFiles.next();
    updateSnapshotDocument_(file.getId(), content);
    return file;
  }

  const document = DocumentApp.create(CONFIG.snapshotDocumentName);
  document.getBody().setText(content);
  document.saveAndClose();

  const file = DriveApp.getFileById(document.getId());
  file.moveTo(snapshotsFolder);
  return file;
}

function updateSnapshotDocument_(documentId, content) {
  const document = DocumentApp.openById(documentId);
  document.getBody().setText(content);
  document.saveAndClose();
}

function findOrCreateFolder_(parentFolder, folderName) {
  const folders = parentFolder.getFoldersByName(folderName);

  if (folders.hasNext()) {
    return folders.next();
  }

  return parentFolder.createFolder(folderName);
}

function parseSince_(since) {
  if (!since) {
    return new Date(Date.now() - (CONFIG.defaultLookbackHours * 60 * 60 * 1000));
  }

  if (since instanceof Date) {
    return since;
  }

  if (typeof since === 'number') {
    return new Date(since);
  }

  if (typeof since === 'string') {
    const parsed = new Date(since);

    if (!isNaN(parsed.getTime())) {
      return parsed;
    }
  }

  throw new Error(
    'Invalid "since" value. Use ISO-8601, Date, or epoch milliseconds.'
  );
}

function resolveAccount_() {
  const effectiveEmail = Session.getEffectiveUser().getEmail();

  if (effectiveEmail) {
    return effectiveEmail;
  }

  const activeEmail = Session.getActiveUser().getEmail();

  if (activeEmail) {
    return activeEmail;
  }

  return CONFIG.expectedAccount;
}

function validateExpectedAccount_(detectedAccount) {
  if (!detectedAccount) {
    return;
  }

  if (detectedAccount.toLowerCase() !== CONFIG.expectedAccount.toLowerCase()) {
    throw new Error(
      'This script expects ' + CONFIG.expectedAccount + ' but is running as ' + detectedAccount + '.'
    );
  }
}

function buildSelfAddressSet_(account) {
  const addresses = {};
  const aliases = GmailApp.getAliases();
  const knownAddresses = [CONFIG.expectedAccount, account].concat(aliases);

  knownAddresses.forEach(function addAddress(email) {
    if (!email) {
      return;
    }
    addresses[email.toLowerCase()] = true;
  });

  return addresses;
}

function isIncomingMessage_(message, selfAddresses) {
  const from = extractEmail_(message.getFrom());

  if (!from) {
    return true;
  }

  return !selfAddresses[from.toLowerCase()];
}

function extractEmail_(raw) {
  const match = String(raw || '').match(/<([^>]+)>/);

  if (match && match[1]) {
    return match[1].trim();
  }

  const plain = String(raw || '').trim();

  if (plain.indexOf('@') !== -1) {
    return plain;
  }

  return '';
}

function buildSnippet_(plainBody) {
  return String(plainBody || '')
    .replace(/\s+/g, ' ')
    .trim()
    .slice(0, 200);
}

function safeGetPlainBody_(message) {
  try {
    return message.getPlainBody();
  } catch (error) {
    logError_('Plain body fallback failed', error);
    return '';
  }
}

function resolveEventLocation_(event) {
  const location = String(event.getLocation() || '').trim();

  if (location) {
    return location;
  }

  const description = String(event.getDescription() || '');
  const match = description.match(/https?:\/\/\S+/);

  return match ? match[0] : '';
}

function getAttendeesCount_(event) {
  try {
    return event.getGuestList().length;
  } catch (error) {
    logError_('Guest list failed', error);
    return 0;
  }
}

function toIsoString_(date) {
  return Utilities.formatDate(
    new Date(date),
    Session.getScriptTimeZone(),
    "yyyy-MM-dd'T'HH:mm:ssXXX"
  );
}

function formatError_(error) {
  if (!error) {
    return 'unknown error';
  }

  if (typeof error === 'string') {
    return error;
  }

  return String(error.message || error);
}

function logError_(message, error) {
  console.error(message + ': ' + formatError_(error));
}
