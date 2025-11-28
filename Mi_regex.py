class MisRegex:
    def regex_nombre(self):
        return r"^[A-Za-záéíóúÁÉÍÓÚñÑ ]{2,20}$"

    def regex_apellido(self):
        return r"^[A-Za-záéíóúÁÉÍÓÚñÑ ]{2,20}$"

    def regex_pasaje(self):
        return r"^[A-Za-z0-9]{1,20}$"

    def regex_horario(self):
        return r"^[0-9:]{1,5}$"

    def regex_dni(self):
        return r"^[0-9]{1,10}$"

    def regex_destino(self):
        return r"^[A-Za-záéíóúÁÉÍÓÚñÑ ]{2,20}$"

    def regex_fecha(self):
        return r"^[0-9/-]{1,20}$"