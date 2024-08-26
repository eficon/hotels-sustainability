from enum import Enum


class ExtractionTypes(str, Enum):
    NUMBER = "Número"
    SECTION = "Apartado"
    PHRASE = "Frase"
    WORD = "Palabra"

    def __str__(self):
        return self.value


class Flavor(str, Enum):
    EMPRESA = "Empresa"
    BOOKING = "Booking"
    GOOGLE = "Google"

    def __str__(self):
        return self.value


BookingSustainabilityMapping = {
    "Booking_Certificados_Sostenibilidad": "pp_sustainability_cert",
    "Booking_Residuos": "pp_sustainability_block_waste",
    "Booking_Agua": "pp_sustainability_block_water",
    "Booking_Energía": "pp_sustainability_block_greenhouse",
    "Booking_Destino": "pp_sustainability_block_community",
    "Booking_Naturaleza": "pp_sustainability_block_eco",
}

BookingPropertySustainabilityTextMapping = {
    "pp_sustainability_block_community_art": "Los artistas locales pueden exponer sus obras aquí",
    "pp_sustainability_block_community_ecosystem": "El alojamiento proporciona información sobre los ecosistemas, el patrimonio y la cultura locales, y sobre el comportamiento esperado",
    "pp_sustainability_block_community_invest": "El alojamiento invierte un porcentaje de los ingresos en proyectos de sostenibilidad o de la comunidad",
    "pp_sustainability_block_community_tours": "Se ofrecen tours y actividades organizados por empresas y guías locales",
    "pp_sustainability_block_eco_green_space": "El alojamiento tiene espacios verdes, como jardín o azotea verde",
    "pp_sustainability_block_eco_organic_food": "La mayoría de la comida que se sirve es ecológica",
    "pp_sustainability_block_eco_wildlife": "No se exhiben ni se interactúa con animales salvajes (no domesticados) mantenidos en cautividad en el alojamiento, tampoco se consumen, se venden ni se cazan o matan con otros fines",
    "pp_sustainability_block_greenhouse_bike_parking": "Hay parking de bicicletas",
    "pp_sustainability_block_greenhouse_bike_rent": "Se alquilan bicicletas",
    "pp_sustainability_block_greenhouse_carbon": "El alojamiento compensa una parte de su huella de carbono",
    "pp_sustainability_block_greenhouse_electric_car": "Hay un punto de carga para coches eléctricos",
    "pp_sustainability_block_greenhouse_energy": "Toda la electricidad procede de energías renovables",
    "pp_sustainability_block_greenhouse_keycard": "La electricidad funciona con sensor de movimiento o tarjeta",
    "pp_sustainability_block_greenhouse_lights": "La mayoría de las luces del alojamiento usan bombillas LED (de bajo consumo)",
    "pp_sustainability_block_greenhouse_seasonal_food": "La mayoría de la comida del alojamiento procede de la zona",
    "pp_sustainability_block_greenhouse_window": "Todas las ventanas son de doble acristalamiento",
    "pp_sustainability_block_waste_bins": "Hay papeleras de reciclaje a disposición de los clientes y la basura se recicla",
    "pp_sustainability_block_waste_drink_bottle": "No se utilizan botellas de bebidas de plástico de un solo uso",
    "pp_sustainability_block_waste_food": "El alojamiento trata de reducir el desperdicio alimentario",
    "pp_sustainability_block_waste_mini_toil": "No se utilizan botes mini de plástico de un solo uso para el champú, el acondicionador ni el gel de baño",
    "pp_sustainability_block_waste_plates": "No se utilizan cubiertos ni vajilla de plástico de un solo uso",
    "pp_sustainability_block_waste_reusable_cups": "No se utilizan vasos de plástico de un solo uso",
    "pp_sustainability_block_waste_stirrer": "No se utilizan cucharillas de plástico de un solo uso",
    "pp_sustainability_block_waste_straw": "No se utilizan pajitas de plástico de un solo uso",
    "pp_sustainability_block_waste_water_bottle": "No se utilizan botellas de agua de plástico de un solo uso",
    "pp_sustainability_block_waste_water_cooler": "Hay dispensador/refrigerador de agua",
    "pp_sustainability_block_water_cleaning": "Se puede renunciar a la limpieza diaria de la habitación",
    "pp_sustainability_block_water_shower": "Las duchas usan poca agua",
    "pp_sustainability_block_water_toilet": "Los WC usan poca agua",
    "pp_sustainability_block_water_towel": "Se pueden reutilizar las toallas",
}

BookingPropertySustainabilitySplits = {
    "Booking_Agua_Contexto": {
        "Se puede renunciar a la limpieza diaria de la habitación": "water_cleaning",
        "Las duchas usan poca agua": "water_shower",
        "Los WC usan poca agua": "water_toilet",
        "Se pueden reutilizar las toallas": "water_towel",
    },
    "Booking_Destino_Contexto": {
        "Los artistas locales pueden exponer sus obras aquí": "community_art",
        "El alojamiento proporciona información sobre los ecosistemas, el patrimonio y la cultura locales, y sobre el comportamiento esperado": "community_ecosystem",
        "El alojamiento invierte un porcentaje de los ingresos en proyectos de sostenibilidad o de la comunidad": "community_invest",
        "Se ofrecen tours y actividades organizados por empresas y guías locales": "community_tours",
    },
    "Booking_Energía_Contexto": {
        "Hay parking de bicicletas": "greenhouse_bike_parking",
        "Se alquilan bicicletas": "greenhouse_bike_rent",
        "El alojamiento compensa una parte de su huella de carbono": "greenhouse_carbon",
        "Hay un punto de carga para coches eléctricos": "greenhouse_electric_car",
        "Toda la electricidad procede de energías renovables": "greenhouse_energy",
        "La electricidad funciona con sensor de movimiento o tarjeta": "greenhouse_keycard",
        "La mayoría de las luces del alojamiento usan bombillas LED (de bajo consumo)": "greenhouse_lights",
        "La mayoría de la comida del alojamiento procede de la zona": "greenhouse_seasonal_food",
        "Todas las ventanas son de doble acristalamiento": "greenhouse_window",
    },
    "Booking_Naturaleza_Contexto": {
        "El alojamiento tiene espacios verdes, como jardín o azotea verde": "eco_green_space",
        "La mayoría de la comida que se sirve es ecológica": "eco_organic_food",
        "No se exhiben ni se interactúa con animales salvajes (no domesticados) mantenidos en cautividad en el alojamiento, tampoco se consumen, se venden ni se cazan o matan con otros fines": "eco_wildlife",
    },
    "Booking_Residuos_Contexto": {
        "Hay papeleras de reciclaje a disposición de los clientes y la basura se recicla": "waste_bins",
        "No se utilizan botellas de bebidas de plástico de un solo uso": "waste_drink_bottle",
        "El alojamiento trata de reducir el desperdicio alimentario": "waste_food",
        "No se utilizan botes mini de plástico de un solo uso para el champú, el acondicionador ni el gel de baño": "waste_mini_toil",
        "No se utilizan cubiertos ni vajilla de plástico de un solo uso": "waste_plates",
        "No se utilizan vasos de plástico de un solo uso": "waste_reusable_cups",
        "No se utilizan cucharillas de plástico de un solo uso": "waste_stirrer",
        "No se utilizan pajitas de plástico de un solo uso": "waste_straw",
        "No se utilizan botellas de agua de plástico de un solo uso": "waste_water_bottle",
        "Hay dispensador/refrigerador de agua": "waste_water_cooler",
    },
}

BookingPropertySustainabilityFacilityMapping = {
    '182': "pp_sustainability_block_greenhouse_electric_car",  # 'Estación de carga de vehículos eléctricos'
    '426': "pp_sustainability_block_greenhouse_bike_parking",  # 'Parking de bicicletas'
    '435': "pp_sustainability_block_waste_mini_toil",
    # '¿Has eliminado los botes mini de champú, acondicionador y gel de un solo uso (o nunca los has usado)?'
    '436': "pp_sustainability_block_water_towel",  # 'Los clientes pueden reutilizar las toallas'
    '439': "pp_sustainability_block_waste_straw",  # '¿Has eliminado las pajitas de plástico (o nunca las has usado)?'
    '440': "pp_sustainability_block_waste_reusable_cups",
    # '¿Has eliminado los vasos de plástico (o nunca los has usado)?'
    '441': "pp_sustainability_block_waste_water_bottle",
    # '¿Has eliminado las botellas de agua de plástico (o nunca las has usado)?'
    '442': "pp_sustainability_block_waste_drink_bottle",
    # '¿Has eliminado las otras botellas de plástico (o nunca las has usado)?'
    '443': "pp_sustainability_block_waste_plates",
    # '¿Has eliminado los cubiertos y la vajilla de plástico (o nunca los has usado)?'
    '444': "pp_sustainability_block_greenhouse_keycard",
    # 'Electricidad con sensor de movimiento o tarjeta para clientes'
    '445': "pp_sustainability_block_water_cleaning",  # 'Los clientes pueden renunciar al servicio de limpieza diaria'
    '446': "pp_sustainability_block_waste_water_cooler",  # 'Dispensador/refrigerador de agua'
    '447': "pp_sustainability_block_greenhouse_bike_rent",  # 'Alquiler de bicicletas'
    '448': "pp_sustainability_block_waste_stirrer",
    # '¿Has eliminado las cucharillas de plástico (o nunca las has usado)?'
    '489': "pp_sustainability_block_eco_wildlife",
    # 'No se exhiben ni se interactúa con animales salvajes (no domesticados) mantenidos en cautividad en el alojamiento, tampoco se consumen, se venden ni se cazan o matan con otros fines'
    '490': "pp_sustainability_block_waste_bins",
    # 'Hay papeleras de reciclaje a disposición de los clientes y la basura se recicla'
    '491': "pp_sustainability_block_greenhouse_seasonal_food",  # 'Al menos el 80% de la comida procede de tu región'
    '492': "pp_sustainability_block_greenhouse_lights",
    # 'Al menos el 80% de las luces usan bombillas LED (de bajo consumo)'
    '493': "pp_sustainability_block_water_toilet",
    # 'Solo hay WC de bajo consumo de agua (de doble descarga o descarga reducida)'
    '494': "pp_sustainability_block_water_shower",
    # 'Solo hay duchas de bajo consumo de agua (duchas inteligentes o de poco flujo)'
    '495': "pp_sustainability_block_greenhouse_window",  # 'Todas las ventanas son de doble acristalamiento'
    '496': "pp_sustainability_block_waste_food",
    # 'Para combatir el desperdicio alimentario, tomas medidas de prevención, reducción, reciclaje, concienciación y eliminación'
    '497': "pp_sustainability_block_community_invest",
    # 'Inviertes un porcentaje de los ingresos en proyectos de sostenibilidad o de la comunidad'
    '498': "pp_sustainability_block_greenhouse_carbon",
    # 'Compensas al menos un 10% del total de tus emisiones de carbono anuales comprando créditos de carbono certificados'
    '499': "pp_sustainability_block_community_tours",
    # 'Se ofrecen tours y actividades organizados por empresas y guías locales'
    '502': "pp_sustainability_block_eco_green_space",
    # 'El alojamiento tiene espacios verdes, como jardín o azotea verde'
    '503': "pp_sustainability_block_eco_organic_food",  # 'Al menos el 80% de la comida es ecológica'
    '504': "pp_sustainability_block_greenhouse_energy",
    # 'Toda la electricidad del alojamiento procede de energías renovables'
    '505': "pp_sustainability_block_community_art",  # 'Los artistas locales pueden exponer sus obras aquí'
    '506': "pp_sustainability_block_community_ecosystem",
    # 'Los clientes reciben información sobre los ecosistemas, el patrimonio y la cultura locales, y sobre el comportamiento esperado'
}

BookingColumnsIndicators = ['community_art', 'community_ecosystem', 'community_invest', 'community_tours',
                            'eco_green_space', 'eco_organic_food', 'eco_wildlife', 'greenhouse_bike_parking',
                            'greenhouse_bike_rent', 'greenhouse_carbon', 'greenhouse_electric_car', 'greenhouse_energy',
                            'greenhouse_keycard', 'greenhouse_lights', 'greenhouse_seasonal_food', 'greenhouse_window',
                            'waste_bins', 'waste_drink_bottle', 'waste_food', 'waste_mini_toil', 'waste_plates',
                            'waste_reusable_cups', 'waste_stirrer', 'waste_straw', 'waste_water_bottle',
                            'waste_water_cooler', 'water_cleaning', 'water_shower', 'water_toilet', 'water_towel']
