package utils

var CountryToCurrency = map[string]string{
	"AE":                                "AED", // United Arab Emirates
	"AF":                                "AFN", // Afghanistan
	"AL":                                "ALL", // Albania
	"AM":                                "AMD", // Armenia
	"AN":                                "ANG", // Netherlands Antilles
	"AO":                                "AOA", // Angola
	"AR":                                "ARS", // Argentina
	"AU":                                "AUD", // Australia
	"AW":                                "AWG", // Aruba
	"AZ":                                "AZN", // Azerbaijan
	"BA":                                "BAM", // Bosnia and Herzegovina
	"BB":                                "BBD", // Barbados
	"BD":                                "BDT", // Bangladesh
	"BG":                                "BGN", // Bulgaria
	"BH":                                "BHD", // Bahrain
	"BI":                                "BIF", // Burundi
	"BM":                                "BMD", // Bermuda
	"BN":                                "BND", // Brunei
	"BO":                                "BOB", // Bolivia
	"BR":                                "BRL", // Brazil
	"BS":                                "BSD", // Bahamas
	"BT":                                "BTN", // Bhutan
	"BW":                                "BWP", // Botswana
	"BY":                                "BYN", // Belarus
	"BZ":                                "BZD", // Belize
	"CA":                                "CAD", // Canada
	"CD":                                "CDF", // Democratic Republic of the Congo
	"CH":                                "CHF", // Switzerland
	"CL":                                "CLP", // Chile
	"CN":                                "CNY", // China
	"CO":                                "COP", // Colombia
	"CR":                                "CRC", // Costa Rica
	"CU":                                "CUP", // Cuba
	"CV":                                "CVE", // Cape Verde
	"CZ":                                "CZK", // Czech Republic
	"DJ":                                "DJF", // Djibouti
	"DK":                                "DKK", // Denmark
	"DO":                                "DOP", // Dominican Republic
	"DZ":                                "DZD", // Algeria
	"EG":                                "EGP", // Egypt
	"ER":                                "ERN", // Eritrea
	"ET":                                "ETB", // Ethiopia
	"EU":                                "EUR", // Eurozone
	"FJ":                                "FJD", // Fiji
	"FK":                                "FKP", // Falkland Islands
	"FO":                                "FOK", // Faroe Islands
	"GB":                                "GBP", // United Kingdom
	"GE":                                "GEL", // Georgia
	"GG":                                "GGP", // Guernsey
	"GH":                                "GHS", // Ghana
	"GI":                                "GIP", // Gibraltar
	"GM":                                "GMD", // Gambia
	"GN":                                "GNF", // Guinea
	"GT":                                "GTQ", // Guatemala
	"GY":                                "GYD", // Guyana
	"HK":                                "HKD", // Hong Kong
	"HN":                                "HNL", // Honduras
	"HR":                                "HRK", // Croatia
	"HT":                                "HTG", // Haiti
	"HU":                                "HUF", // Hungary
	"ID":                                "IDR", // Indonesia
	"IL":                                "ILS", // Israel
	"IM":                                "IMP", // Isle of Man
	"IN":                                "INR", // India
	"IQ":                                "IQD", // Iraq
	"IR":                                "IRR", // Iran
	"IS":                                "ISK", // Iceland
	"JE":                                "JEP", // Jersey
	"JM":                                "JMD", // Jamaica
	"JO":                                "JOD", // Jordan
	"JP":                                "JPY", // Japan
	"KE":                                "KES", // Kenya
	"KG":                                "KGS", // Kyrgyzstan
	"KH":                                "KHR", // Cambodia
	"KI":                                "KID", // Kiribati
	"KM":                                "KMF", // Comoros
	"KR":                                "KRW", // South Korea
	"KW":                                "KWD", // Kuwait
	"KY":                                "KYD", // Cayman Islands
	"KZ":                                "KZT", // Kazakhstan
	"LA":                                "LAK", // Laos
	"LB":                                "LBP", // Lebanon
	"LK":                                "LKR", // Sri Lanka
	"LR":                                "LRD", // Liberia
	"LS":                                "LSL", // Lesotho
	"LY":                                "LYD", // Libya
	"MA":                                "MAD", // Morocco
	"MD":                                "MDL", // Moldova
	"MG":                                "MGA", // Madagascar
	"MK":                                "MKD", // North Macedonia
	"MM":                                "MMK", // Myanmar
	"MN":                                "MNT", // Mongolia
	"MO":                                "MOP", // Macau
	"MR":                                "MRU", // Mauritania
	"MU":                                "MUR", // Mauritius
	"MV":                                "MVR", // Maldives
	"MW":                                "MWK", // Malawi
	"MX":                                "MXN", // Mexico
	"MY":                                "MYR", // Malaysia
	"MZ":                                "MZN", // Mozambique
	"NA":                                "NAD", // Namibia
	"NG":                                "NGN", // Nigeria
	"NI":                                "NIO", // Nicaragua
	"NO":                                "NOK", // Norway
	"NP":                                "NPR", // Nepal
	"NZ":                                "NZD", // New Zealand
	"OM":                                "OMR", // Oman
	"PA":                                "PAB", // Panama
	"PE":                                "PEN", // Peru
	"PG":                                "PGK", // Papua New Guinea
	"PH":                                "PHP", // Philippines
	"PK":                                "PKR", // Pakistan
	"PL":                                "PLN", // Poland
	"PY":                                "PYG", // Paraguay
	"QA":                                "QAR", // Qatar
	"RO":                                "RON", // Romania
	"RS":                                "RSD", // Serbia
	"RU":                                "RUB", // Russia
	"RW":                                "RWF", // Rwanda
	"SA":                                "SAR", // Saudi Arabia
	"SB":                                "SBD", // Solomon Islands
	"SC":                                "SCR", // Seychelles
	"SD":                                "SDG", // Sudan
	"SE":                                "SEK", // Sweden
	"SG":                                "SGD", // Singapore
	"SH":                                "SHP", // Saint Helena
	"SL":                                "SLE", // Sierra Leone
	"SO":                                "SOS", // Somalia
	"SR":                                "SRD", // Suriname
	"SS":                                "SSP", // South Sudan
	"ST":                                "STN", // São Tomé and Príncipe
	"SY":                                "SYP", // Syria
	"SZ":                                "SZL", // Eswatini
	"TH":                                "THB", // Thailand
	"TJ":                                "TJS", // Tajikistan
	"TM":                                "TMT", // Turkmenistan
	"TN":                                "TND", // Tunisia
	"TO":                                "TOP", // Tonga
	"TR":                                "TRY", // Turkey
	"TT":                                "TTD", // Trinidad and Tobago
	"TV":                                "TVD", // Tuvalu
	"TW":                                "TWD", // Taiwan
	"TZ":                                "TZS", // Tanzania
	"UA":                                "UAH", // Ukraine
	"UG":                                "UGX", // Uganda
	"US":                                "USD", // United States
	"UY":                                "UYU", // Uruguay
	"UZ":                                "UZS", // Uzbekistan
	"VE":                                "VES", // Venezuela
	"VN":                                "VND", // Vietnam
	"VU":                                "VUV", // Vanuatu
	"WS":                                "WST", // Samoa
	"X1":                                "XAF", // Central African CFA franc
	"X2":                                "XCD", // Eastern Caribbean dollar
	"X3":                                "XDR", // International Monetary Fund
	"X4":                                "XOF", // West African CFA franc
	"X5":                                "XPF", // CFP franc
	"YE":                                "YER", // Yemen
	"ZA":                                "ZAR", // South Africa
	"ZM":                                "ZMW", // Zambia
	"ZW":                                "ZWL", // Zimbabwe
	"United Arab Emirates":              "AED",
	"Afghanistan":                       "AFN",
	"Albania":                           "ALL",
	"Armenia":                           "AMD",
	"Netherlands Antilles":              "ANG",
	"Angola":                            "AOA",
	"Argentina":                         "ARS",
	"Australia":                         "AUD",
	"Aruba":                             "AWG",
	"Azerbaijan":                        "AZN",
	"Bosnia and Herzegovina":            "BAM",
	"Barbados":                          "BBD",
	"Bangladesh":                        "BDT",
	"Bulgaria":                          "BGN",
	"Bahrain":                           "BHD",
	"Burundi":                           "BIF",
	"Bermuda":                           "BMD",
	"Brunei":                            "BND",
	"Bolivia":                           "BOB",
	"Brazil":                            "BRL",
	"Bahamas":                           "BSD",
	"Bhutan":                            "BTN",
	"Botswana":                          "BWP",
	"Belarus":                           "BYN",
	"Belize":                            "BZD",
	"Canada":                            "CAD",
	"Democratic Republic of the Congo":  "CDF",
	"Switzerland":                       "CHF",
	"Chile":                             "CLP",
	"China":                             "CNY",
	"Colombia":                          "COP",
	"Costa Rica":                        "CRC",
	"Cuba":                              "CUP",
	"Cape Verde":                        "CVE",
	"Czech Republic":                    "CZK",
	"Djibouti":                          "DJF",
	"Denmark":                           "DKK",
	"Dominican Republic":                "DOP",
	"Algeria":                           "DZD",
	"Egypt":                             "EGP",
	"Eritrea":                           "ERN",
	"Ethiopia":                          "ETB",
	"Eurozone":                          "EUR",
	"Fiji":                              "FJD",
	"Falkland Islands":                  "FKP",
	"Faroe Islands":                     "FOK",
	"United Kingdom":                    "GBP",
	"Georgia":                           "GEL",
	"Guernsey":                          "GGP",
	"Ghana":                             "GHS",
	"Gibraltar":                         "GIP",
	"Gambia":                            "GMD",
	"Guinea":                            "GNF",
	"Guatemala":                         "GTQ",
	"Guyana":                            "GYD",
	"Hong Kong":                         "HKD",
	"Honduras":                          "HNL",
	"Croatia":                           "HRK",
	"Haiti":                             "HTG",
	"Hungary":                           "HUF",
	"Indonesia":                         "IDR",
	"Israel":                            "ILS",
	"Isle of Man":                       "IMP",
	"India":                             "INR",
	"Iraq":                              "IQD",
	"Iran":                              "IRR",
	"Iceland":                           "ISK",
	"Jersey":                            "JEP",
	"Jamaica":                           "JMD",
	"Jordan":                            "JOD",
	"Japan":                             "JPY",
	"Kenya":                             "KES",
	"Kyrgyzstan":                        "KGS",
	"Cambodia":                          "KHR",
	"Kiribati":                          "KID",
	"Comoros":                           "KMF",
	"South Korea":                       "KRW",
	"Kuwait":                            "KWD",
	"Cayman Islands":                    "KYD",
	"Kazakhstan":                        "KZT",
	"Laos":                              "LAK",
	"Lebanon":                           "LBP",
	"Sri Lanka":                         "LKR",
	"Liberia":                           "LRD",
	"Lesotho":                           "LSL",
	"Libya":                             "LYD",
	"Morocco":                           "MAD",
	"Moldova":                           "MDL",
	"Madagascar":                        "MGA",
	"North Macedonia":                   "MKD",
	"Myanmar":                           "MMK",
	"Mongolia":                          "MNT",
	"Macau":                             "MOP",
	"Mauritania":                        "MRU",
	"Mauritius":                         "MUR",
	"Maldives":                          "MVR",
	"Malawi":                            "MWK",
	"Mexico":                            "MXN",
	"Malaysia":                          "MYR",
	"Mozambique":                        "MZN",
	"Namibia":                           "NAD",
	"Nigeria":                           "NGN",
	"Nicaragua":                         "NIO",
	"Norway":                            "NOK",
	"Nepal":                             "NPR",
	"New Zealand":                       "NZD",
	"Oman":                              "OMR",
	"Panama":                            "PAB",
	"Peru":                              "PEN",
	"Papua New Guinea":                  "PGK",
	"Philippines":                       "PHP",
	"Pakistan":                          "PKR",
	"Poland":                            "PLN",
	"Paraguay":                          "PYG",
	"Qatar":                             "QAR",
	"Romania":                           "RON",
	"Serbia":                            "RSD",
	"Russia":                            "RUB",
	"Rwanda":                            "RWF",
	"Saudi Arabia":                      "SAR",
	"Solomon Islands":                   "SBD",
	"Seychelles":                        "SCR",
	"Sudan":                             "SDG",
	"Sweden":                            "SEK",
	"Singapore":                         "SGD",
	"Saint Helena":                      "SHP",
	"Sierra Leone":                      "SLE",
	"Somalia":                           "SOS",
	"Suriname":                          "SRD",
	"South Sudan":                       "SSP",
	"São Tomé and Príncipe":             "STN",
	"Syria":                             "SYP",
	"Eswatini":                          "SZL",
	"Thailand":                          "THB",
	"Tajikistan":                        "TJS",
	"Turkmenistan":                      "TMT",
	"Tunisia":                           "TND",
	"Tonga":                             "TOP",
	"Turkey":                            "TRY",
	"Trinidad and Tobago":               "TTD",
	"Tuvalu":                            "TVD",
	"Taiwan":                            "TWD",
	"Tanzania":                          "TZS",
	"Ukraine":                           "UAH",
	"Uganda":                            "UGX",
	"United States":                     "USD",
	"Uruguay":                           "UYU",
	"Uzbekistan":                        "UZS",
	"Venezuela":                         "VES",
	"Vietnam":                           "VND",
	"Vanuatu":                           "VUV",
	"Samoa":                             "WST",
	"Central African CFA franc":         "XAF",
	"Eastern Caribbean dollar":          "XCD",
	"International Monetary Fund (IMF)": "XDR",
	"West African CFA franc":            "XOF",
	"CFP franc":                         "XPF",
	"Yemen":                             "YER",
	"South Africa":                      "ZAR",
	"Zambia":                            "ZMW",
	"Zimbabwe":                          "ZWL",
}

var Gw2Times = map[string][]map[string]string{
    "Tyria": {
        {"stage": "Day", "start": "02:30", "end": "03:39"},
        {"stage": "Dusk", "start": "03:40", "end": "03:44"},
        {"stage": "Night", "start": "03:45", "end": "04:24"},
        {"stage": "Dawn", "start": "04:25", "end": "04:29"},
        {"stage": "Day", "start": "04:30", "end": "05:39"},
        {"stage": "Dusk", "start": "05:40", "end": "05:44"},
        {"stage": "Night", "start": "05:45", "end": "18:24"},
        {"stage": "Dawn", "start": "18:25", "end": "18:29"},
        {"stage": "Day", "start": "18:30", "end": "19:39"},
        {"stage": "Dusk", "start": "19:40", "end": "19:44"},
        {"stage": "Night", "start": "19:45", "end": "20:24"},
        {"stage": "Dawn", "start": "20:25", "end": "20:29"},
        {"stage": "Day", "start": "20:30", "end": "21:39"},
        {"stage": "Dusk", "start": "21:40", "end": "21:44"},
        {"stage": "Night", "start": "21:45", "end": "22:24"},
        {"stage": "Dawn", "start": "22:25", "end": "22:29"},
        {"stage": "Day", "start": "22:30", "end": "23:39"},
        {"stage": "Dusk", "start": "23:40", "end": "23:44"},
        {"stage": "Night", "start": "23:45", "end": "00:24"},
        {"stage": "Dawn", "start": "00:25", "end": "00:29"},
        {"stage": "Day", "start": "00:30", "end": "01:39"},
        {"stage": "Dusk", "start": "01:40", "end": "01:44"},
        {"stage": "Night", "start": "01:45", "end": "02:24"},
        {"stage": "Dawn", "start": "02:25", "end": "02:29"},
    },
}
