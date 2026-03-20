on pad2(n)
	if n < 10 then
		return "0" & (n as text)
	end if
	return n as text
end pad2

on joinLines(itemsList)
	set AppleScript's text item delimiters to linefeed
	set joined to itemsList as text
	set AppleScript's text item delimiters to ""
	return joined
end joinLines

on reminderLabel(dueDate)
	if dueDate is missing value then
		return "dia inteiro"
	end if
	set hh to hours of dueDate
	set mm to minutes of dueDate
	if hh = 0 and mm = 0 then
		return "dia inteiro"
	end if
	return my pad2(hh) & ":" & my pad2(mm)
end reminderLabel

on run argv
	set action to "fetch"
	if (count of argv) > 0 then
		set action to item 1 of argv
	end if
	set nowDate to current date
	set startOfDay to nowDate - (time of nowDate)
	set endOfDay to startOfDay + (1 * days)
	set outputLines to {}
	
	try
		tell application "Reminders"
			set allLists to lists
			if action is "auth" then
				set statusText to "connected"
			else
				set statusText to "ok"
			end if
			set end of outputLines to "STATUS:" & statusText
			set end of outputLines to "AUTHORIZATION:authorized"
			repeat with oneList in allLists
				set listName to (name of oneList as text)
				set end of outputLines to "LIST:" & listName
			end repeat
			
			if action is "fetch" then
				set foundAny to false
				repeat with oneList in allLists
					set listName to (name of oneList as text)
					set openReminders to (every reminder of oneList whose completed is false)
					repeat with oneReminder in openReminders
						try
							set dueDate to due date of oneReminder
							if dueDate is not missing value then
								if dueDate ≥ startOfDay and dueDate < endOfDay then
									set foundAny to true
									set titleText to (name of oneReminder as text)
									set displayText to (my reminderLabel(dueDate)) & " | [Apple Reminders] " & titleText & " (" & listName & ")"
									set end of outputLines to "ITEM:" & displayText
								end if
							end if
						end try
					end repeat
				end repeat
				if foundAny is false then
					set end of outputLines to "NOTE:Nenhum Apple Reminder vencendo hoje."
				else
					set end of outputLines to "NOTE:Apple Reminders via AppleScript."
				end if
			end if
		end tell
	on error errMsg number errNum
		set outputLines to {"STATUS:error", "AUTHORIZATION:error", "ERROR:" & errNum & " | " & errMsg}
	end try
	
	return my joinLines(outputLines)
end run
