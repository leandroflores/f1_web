export function decimal(v: string) {
  const test = /^\d*(\.\d{0,2})?$/.test(v);
  return test || "Número inválido. Formato esperado: 1,23";
}

export function required(v: any) {
  return (typeof v == "number" && v == 0) || !!v || "Campo obrigatório";
}

export function requiredMultiple(v: any) {
  return v.length > 0 || "Campo obrigatório";
}

export function validateEmail(v: string) {
  const test = /^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/.test(v);
  return test || "Email inválido. Formato esperado: seu@email.com";
}

export function validateCpf(v: string) {
  const test = /^(\d{3}\.\d{3}\.\d{3}-\d{2})$/.test(v);
  return test || "CPF inválido. Formato esperado: XXX.XXX.XXX-XX";
}

export function validateCnpj(v: string) {
  const test = /^(\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2})$/.test(v);
  return test || "CNPJ inválido. Formato esperado: XX.XXX.XXX/XXXX-XX";
}

export function validatePassword(v: string) {
  if (!v) return true;
  const re = /^(?=.*\d)(?=.*[!@#$%^&*.])(?=.*[a-z])(?=.*[A-Z]).{8,}$/;
  return (
    re.test(v) ||
    "A Senha deve conter 8 ou mais caracteres, com pelo menos uma letra maiúscula, uma minúscula, um caractere especial (!@#$%^&*.) e um número. Ex: Abcd531@"
  );
}

export function minValue(min: number) {
  return (v: number) => v >= min || `Deve ser maior ou igual a ${min}`;
}
