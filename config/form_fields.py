from phonenumber_field.formfields import PhoneNumberField as _PhoneNumberField


class PhoneNumberField(_PhoneNumberField):
    def to_python(self, value):
        if value.startswith("0"):
            value = f"+234{value[1:]}"
        else:
            value = f"+234{value}"
        return super().to_python(value)
