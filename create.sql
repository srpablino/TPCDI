CREATE TABLE dimdate (
         SK_DateID            NUMBER PRIMARY KEY,
         DateValue            DATE NOT NULL,
         DateDesc             VARCHAR2(20) NOT NULL,
         CalendarYearID       NUMBER NOT NULL,
         CalendarYearDesc     VARCHAR2(20) NOT NULL,
         CalendarQtrID        NUMBER NOT NULL,
         CalendarQtrDesc      VARCHAR2(20) NOT NULL,
         CalendarMonthID      NUMBER NOT NULL,
         CalendarMonthDesc    VARCHAR2(20) NOT NULL,
         CalendarWeekID       NUMBER NOT NULL,
         CalendarWeekDesc     VARCHAR2(20) NOT NULL,
         DayOfWeekNum         NUMBER NOT NULL,
         DayOfWeekDesc        VARCHAR2(10) NOT NULL,
         FiscalYearID         NUMBER NOT NULL,
         FiscalYearDesc       VARCHAR2(20) NOT NULL,
         FiscalQtrID          NUMBER NOT NULL,
         FiscalQtrDesc        VARCHAR2(20) NOT NULL,
         HolidayFlag          CHAR(1 byte)
         );

CREATE TABLE dimbroker(
SK_BrokerID          NUMBER PRIMARY KEY,
BrokerID             NUMBER NOT NULL,
ManagerID            NUMBER,
FirstName            VARCHAR2(50) NOT NULL,
LastName             VARCHAR2(50) NOT NULL,
MiddleInitial        VARCHAR2(1),
Branch               VARCHAR2(50),
Office               VARCHAR2(50),
Phone                VARCHAR2(14),
IsCurrent            CHAR(1 byte) NOT NULL,
BatchID              NUMBER NOT NULL,
EffectiveDate        DATE NOT NULL,
EndDate              DATE NOT NULL 
);

CREATE TABLE DIMTIME 
(
  SK_TIMEID NUMBER NOT NULL 
, TIMEVALUE TIMESTAMP NOT NULL 
, HOURID NUMBER(2) NOT NULL 
, HOURDESC VARCHAR2(20) NOT NULL 
, MINUTEID NUMBER(2) NOT NULL 
, MINUTEDESC VARCHAR2(20) NOT NULL 
, SECONDID NUMBER(2) NOT NULL 
, SECONDDESC VARCHAR2(20) NOT NULL 
, MARKETHOURSFLAG CHAR(1) 
, OFFICEHOURSFLAG CHAR(1) 
, CONSTRAINT DIMTIME_PK PRIMARY KEY 
  (
    SK_TIMEID 
  )
  ENABLE 
);

