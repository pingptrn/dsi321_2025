{
  "columns": [
    "timestamp", "stationID", "nameTH", "nameEN", "areaTH", "areaEN",
    "stationType", "lat", "long", "PM25.color_id", "PM25.aqi",
    "year", "month", "day", "hour"
    ],
  "types": [
    "datetime64[ns]", "string", "string", "string", "string", "string",
    "string", "float64", "float64", "int64", "float64",
    "int64", "int64", "int32", "int32"
  ],
  "key_columns": [
    "timestamp", "stationID", "nameTH", "nameEN", "areaTH", "areaEN",
    "stationType", "lat", "long", "PM25.color_id",
    "year", "month", "day", "hour"
  ]
}
