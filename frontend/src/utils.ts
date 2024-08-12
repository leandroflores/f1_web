import dayjs from "dayjs";

export function formatDecimal(value: number) {
  return value.toLocaleString("pt-BR", {
    maximumFractionDigits: 2,
  });
}

export function differenceInHoursMinutes(
  dateString1: string,
  dateString2: string
) {
  const date1 = dayjs(dateString1);
  const date2 = dayjs(dateString2);
  const diff = date2.diff(date1, "minute");
  if (diff < 60) return `${diff}m`;
  if (diff < 60 * 24) return `${Math.floor(diff / 60)}h ${diff % 60}m`;
  return `${Math.floor(diff / 60 / 24)}d ${Math.floor((diff / 60) % 24)}h ${
    diff % 60
  }m`;
}
