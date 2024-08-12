import re
import unicodedata

from datetime import datetime
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hash(object):
    def __init__(self, hash_: str):
        self.hash_value: str = str(hash_)

    def __eq__(self, candidate: str):
        return pwd_context.verify(candidate, self.hash_value)

    def __repr__(self):
        return f"<{type(self).__name__}>: {self.hash_value}"

    @classmethod
    def new(cls, password: str):
        return cls(pwd_context.hash(password))


def update_object(obj: object, new_data: dict, custom_fields: dict = {}):
    for key, value in new_data.items():
        if key in custom_fields:
            setattr(obj, key, custom_fields[key])
            continue
        setattr(obj, key, value)
    return obj


def get_str_value(data: dict, key: str) -> str:
    value: str = data.get(key, "")
    if value:
        return value
    return ""


def get_dict_value(data: dict, key: str) -> dict:
    if key in data:
        return data[key]

    for _, value in data.items():
        if isinstance(value, dict):
            result = get_dict_value(value, key)
            if result is not None:
                return result
    return {}


def date_to_br_format(date: str) -> str:
    try:
        data_obj = datetime.strptime(date, "%Y-%m-%d")
        return data_obj.strftime("%d/%m/%Y")
    except Exception:
        return ""


def str_to_decimal_formatted(content: str) -> str:
    try:
        value: float = float(content)
        str_value: str = f"{value:,.2f}"
        return str_value.replace(",", "X").replace(".", ",").replace("X", ".")
    except Exception:
        return ""


def get_short_name(full_name: str) -> str:
    short_name: str = ""
    if len(full_name) > 0:
        for nome in full_name.split(" "):
            if len(short_name) > 0:
                short_name += " "
            short_name += f"{nome[0]}."
    return short_name


def remove_special_chars(text: str) -> str:
    return "".join(
        character
        for character in unicodedata.normalize("NFKD", text)
        if not unicodedata.combining(character)
    )


def cpf_formatted(cpf: str) -> str:
    try:
        cpf: str = re.sub(r"\D", "", cpf)
        return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
    except Exception:
        return cpf


def cnpj_formatted(cnpj: str) -> str:
    try:
        cnpj: str = re.sub(r"\D", "", cnpj)
        return f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}"
    except Exception:
        return cnpj


def phone_formatted(phone: str) -> str:
    try:
        phone: str = re.sub(r"\D", "", phone)
        if len(phone) == 8:
            return f"{phone[:4]}-{phone[4:]}"
        return f"{phone[:5]}-{phone[5:]}"
    except Exception:
        return phone


def zip_code_formatted(zip_code: str) -> str:
    try:
        zip_code: str = re.sub(r"\D", "", zip_code)
        return f"{zip_code[:5]}-{zip_code[5:]}"
    except Exception:
        return zip_code


def get_str(data: dict, key: str) -> str:
    return str(data.get(key, "") or "")

def get_document_format(value: str) -> str:
    if len(value) == 11:
        return f"{value[:3]}.{value[3:6]}.{value[6:9]}-{value[9:]}"
    if len(value) == 14:
        return f"{value[:2]}.{value[2:5]}.{value[5:8]}/{value[8:12]}-{value[12:]}"
    return value