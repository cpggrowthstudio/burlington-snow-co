// Burlington Snow Co. website bookings -> Google Sheet (+ email alert).
// Paste into Extensions > Apps Script in the "Burlington Snow Co. Bookings" sheet,
// then Deploy > New deployment > Web app (Execute as: Me, Who has access: Anyone).
const SHEET_ID = '1lPibWjRRWHVdBRPI29poO5j1y0mLWZEfkKUDlGatYFY';
const ALERT_EMAIL = Session.getEffectiveUser().getEmail();

function clean(v) {
  v = String(v || '').slice(0, 500);
  return /^[=+\-@]/.test(v) ? "'" + v : v; // stop spreadsheet formulas
}

function doPost(e) {
  const p = e.parameter;
  const row = [new Date(), p.name, p.phone, p.address, p.package, p.price, p.start, p.notes].map((v, i) => i ? clean(v) : v);
  SpreadsheetApp.openById(SHEET_ID).getSheets()[0].appendRow(row.concat('New'));
  MailApp.sendEmail(ALERT_EMAIL, 'New snow booking: ' + clean(p.name),
    ['Name: ' + p.name, 'Phone: ' + p.phone, 'Address: ' + p.address, 'Package: ' + p.package,
     'Price: ' + p.price, 'Start: ' + p.start, 'Notes: ' + (p.notes || '')].join('\n'));
  return ContentService.createTextOutput('ok');
}
