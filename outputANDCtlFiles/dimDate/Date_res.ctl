LOAD DATA
INFILE 'Date_res.txt'
APPEND
INTO TABLE datedim
FIELDS TERMINATED BY '|'
TRAILING NULLCOLS
(
   SK_DateID,
   DateValue DATE "YYYY-MM-DD",
   DateDesc,
   CalendarYearID,
   CalendarYearDesc,
   CalendarQtrID,
   CalendarQtrDesc,
   CalendarMonthID,
   CalendarMonthDesc,
   CalendarWeekID,
   CalendarWeekDesc,
   DayOfWeekNum,
   DayOfWeekDesc,
   FiscalYearID,
   FiscalYearDesc,
   FiscalQtrID,
   FiscalQtrDesc,
   HolidayFlag
)
