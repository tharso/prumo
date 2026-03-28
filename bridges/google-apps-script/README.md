# Bridge: Google Apps Script snapshots multi-conta

Este material existe para uma coisa específica: manter a ponte multi-conta viva sem fingir que ela virou a direção principal da integração Google no runtime.

Pelo [ADR-001-GOOGLE-INTEGRATION.md](/Users/tharsovieira/Documents/DailyLife/Prumo/ADR-001-GOOGLE-INTEGRATION.md), a direção estrutural do runtime é Google APIs diretas. Apps Script + Drive continua valendo como:

1. ponte pragmática;
2. fallback host-neutral;
3. saída de curto prazo para multi-conta sem depender de MCP temperamental.

Não vale tratá-lo como:

1. espinha dorsal definitiva do runtime;
2. desculpa para manter briefing acoplado ao Cowork;
3. camada “provisória” que mora em pasta ignorada e ninguém mais consegue auditar.

## Artefatos rastreáveis

1. [apps-script-setup.md](/Users/tharsovieira/Documents/DailyLife/Prumo/bridges/google-apps-script/apps-script-setup.md)
2. [email-snapshot-personal-template.gs](/Users/tharsovieira/Documents/DailyLife/Prumo/bridges/google-apps-script/email-snapshot-personal-template.gs)
3. [email-snapshot-work-template.gs](/Users/tharsovieira/Documents/DailyLife/Prumo/bridges/google-apps-script/email-snapshot-work-template.gs)

## Regra de bolso

Se a pergunta for “isso substitui a integração Google do runtime?”, a resposta é não.

Se a pergunta for “isso ainda é uma ponte útil para multi-conta hoje?”, a resposta é sim.
