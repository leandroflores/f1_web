const dateTimeFormat = "DD/MM/YYYY HH:mm:ss";
const dateFormat = "DD/MM/YYYY";

const localeDateTimeOptions = {
  month: "2-digit",
  day: "2-digit",
  year: "numeric",
  hour12: false,
  hour: "2-digit",
  minute: "2-digit",
} as const;

const localeDateOptions = {
  month: "2-digit",
  day: "2-digit",
  year: "numeric",
} as const;

export { dateTimeFormat, dateFormat, localeDateOptions, localeDateTimeOptions };
