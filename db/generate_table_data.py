import random
from faker import Faker
from random_username.generate import generate_username
from db import db
import datetime
import requests
import urllib.request
import aiohttp
import asyncio
import secrets
import time
import traceback
import sys
import glob
import os

fake = Faker()
salaries = [10000, 20000, 30000, 40000, 50000, 60000, 70000, 80000, 90000, 10000]
titles = ["Electrician", "Renovation Worker", "Housekeeping Worker", "Plumber", "Gardener"]
language_choices = ['Achinese', 'Acoli', 'Adangme', 'Adyghe', 'Afar', 'Afrihili', 'Afrikaans', 'Aghem', 'Ainu', 'Akan', 'Akkadian', 'Akoose', 'Alabama', 'Albanian', 'Aleut', 'Amarik', 'Angika', 'Arabik', 'Aragonese', 'Aramaic', 'Araona', 'Arapaho', 'Arawak', 'Armenian', 'Aromanian', 'Arpitan', 'Assamese', 'Asturian', 'Asu', 'Atsam', 'Avaric', 'Avestan', 'Awadhi', 'Aymara', 'Azerbaijani', 'Badaga', 'Bafia', 'Bafut', 'Bakhtiari', 'Balinese', 'Baluchi', 'Bambara', 'Bamun', 'Banjar', 'Basaa', 'Bashkir', 'Basque', 'Bavarian', 'Beja', 'Bemba', 'Bena', 'Betawi', 'Bhojpuri', 'Bikol', 'Bini', 'Bishnupriya', 'Bislama', 'Blin', 'Blissymbols', 'Bodo', 'Bosnian', 'Brahui', 'Braj', 'Breton', 'Buginese', 'Bulu', 'Buriat', 'Caddo', 'Cantonese', 'Capiznon', 'Carib', 'Catalan', 'Cayuga', 'Cebuano', 'Chagatai', 'Chamorro', 'Chechen', 'Cherokee', 'Cheyenne', 'Chibcha', 'Chiga', 'Chipewyan', 'Choctaw', 'Chuukese', 'Chuvash', 'Colognian', 'Comorian', 'Coptic', 'Cornish', 'Corsican', 'Cree', 'Creek', 'Croatian', 'Dakota', 'Danish', 'Dargwa', 'Dazaga', 'Delaware', 'Dinka', 'Divehi', 'Dogri', 'Dogrib', 'Duala', 'Dyula', 'Dzongkha', 'Efik', 'Ekajuk', 'Elamite', 'Embu', 'Emilian', 'Erzya', 'Esperanto', 'Estonian', 'Ewe', 'Ewondo', 'Extremaduran', 'Fang', 'Fanti', 'Faroese', 'Fijian', 'Filipino', 'Finnish', 'Flemish', 'Fon', 'Frafra', 'Friulian', 'Fulah', 'Ga', 'Gagauz', 'Galician', 'Ganda', 'Gayo', 'Gbaya', 'Geez', 'Georgian', 'Ghomala', 'Gilaki', 'Gilbertese', 'Gondi', 'Gorontalo', 'Gothic', 'Grebo', 'Guarani', 'Gujarati', 'Gusii', 'Gyaaman', 'Haida', 'Haitian', 'Hausa', 'Hawaiian', 'Hebrew', 'Herero', 'Hiligaynon', 'Hindi', 'Hittite', 'Hmong', 'Hupa', 'Iban', 'Ibibio', 'Icelandic', 'Ido', 'Igbo', 'Iloko', 'Ingrian', 'Ingush', 'Interlingua', 'Interlingue', 'Inuktitut', 'Inupiaq', 'Irish', 'Jju', 'Jutish', 'Kabardian', 'Kabuverdianu', 'Kabyle', 'Kachin', 'Kaingang', 'Kako', 'Kalaallisut', 'Kalenjin', 'Kalmyk', 'Kamba', 'Kanembu', 'Kannada', 'Kanuri', 'Karelian', 'Kashmiri', 'Kashubian', 'Kawi', 'Kazakh', 'Kenyang', 'Khasi', 'Khotanese', 'Khowar', 'Kikuyu', 'Kimbundu', 'Kirmanjki', 'Klingon', 'Kom', 'Komi', 'Kongo', 'Konkani', 'Koro', 'Kosraean', 'Kotava', 'Kpelle', 'Krio', 'Kuanyama', 'Kumyk', 'Kurdish', 'Kurukh', 'Kutenai', 'Kwasio', 'Kyrgyz', 'Ladino', 'Lahnda', 'Lakota', 'Lamba', 'Langi', 'Lao', 'Latgalian', 'Latin', 'Latvian', 'Laz', 'Lezghian', 'Ligurian', 'Limburgish', 'Lingala', 'Lithuanian', 'Livonian', 'Lojban', 'Lombard', 'Lozi', 'Luiseno', 'Lunda', 'Luo', 'Luxembourgish', 'Luyia', 'Maba', 'Macedonian', 'Machame', 'Madurese', 'Mafa', 'Magahi', 'Maithili', 'Makasar', 'Makonde', 'Malagasy', 'Malayalam', 'Maltese', 'Manchu', 'Mandar', 'Mandingo', 'Manipuri', 'Manx', 'Maori', 'Mapuche', 'Marathi', 'Mari', 'Marshallese', 'Marwari', 'Masai', 'Mazanderani', 'Medumba', 'Mende', 'Mentawai', 'Meru', 'Micmac', 'Minangkabau', 'Mingrelian', 'Mirandese', 'Mizo', 'Mohawk', 'Moksha', 'Moldavian', 'Mongo', 'Mongolian', 'Morisyen', 'Mossi', 'Mundang', 'Myene', 'Nama', 'Nauru', 'Navajo', 'Ndonga', 'Neapolitan', 'Newari', 'Ngambay', 'Ngiemboon', 'Ngomba', 'Nheengatu', 'Nias', 'Niuean', 'Nogai', 'Norwegian', 'Novial', 'Nuer', 'Nyamwezi', 'Nyanja', 'Nyankole', 'Nyoro', 'Nzima', 'Occitan', 'Ojibwa', 'Oriya', 'Oromo', 'Osage', 'Ossetic', 'Pahlavi', 'Palauan', 'Pali', 'Pampanga', 'Pangasinan', 'Papiamento', 'Pashto', 'Phoenician', 'Picard', 'Piedmontese', 'Plautdietsch', 'Pohnpeian', 'Pontic', 'Prussian', 'Quechua', 'Rajasthani', 'Rapanui', 'Rarotongan', 'Riffian', 'Romagnol', 'Romansh', 'Romany', 'Rombo', 'Root', 'Rotuman', 'Roviana', 'Rundi', 'Rusyn', 'Rwa', 'Saho', 'Sakha', 'Samburu', 'Samoan', 'Samogitian', 'Sandawe', 'Sango', 'Sangu', 'Sanskrit', 'Santali', 'Sardinian', 'Sasak', 'Saurashtra', 'Scots', 'Selayar', 'Selkup', 'Sena', 'Seneca', 'Serbian', 'Serer', 'Seri', 'Shambala', 'Shan', 'Shona', 'Sicilian', 'Sidamo', 'Siksika', 'Silesian', 'Sindhi', 'Sinhala', 'Slave', 'Slovak', 'Slovenian', 'Soga', 'Sogdien', 'Soninke', 'Sukuma', 'Sumerian', 'Sundanese', 'Susu', 'Swahili', 'Swati', 'Syriac', 'Tachelhit', 'Tagalog', 'Tahitian', 'Taita', 'Tajik', 'Talysh', 'Tamashek', 'Taroko', 'Tasawaq', 'Tatar', 'Telugu', 'Tereno', 'Teso', 'Tetum', 'Tibetan', 'Tigre', 'Tigrinya', 'Timne', 'Tiv', 'Tlingit', 'Tokelau', 'Tongan', 'Tsakhur', 'Tsakonian', 'Tsimshian', 'Tsonga', 'Tswana', 'Tulu', 'Tumbuka', 'Turkmen', 'Turoyo', 'Tuvalu', 'Tuvinian', 'Twi', 'Tyap', 'Udmurt', 'Ugaritic', 'Umbundu', 'Uyghur', 'Uzbek', 'Vai', 'Venda', 'Venetian', 'Veps', 'Votic', 'Vunjo', 'Walloon', 'Walser', 'Waray', 'Warlpiri', 'Washo', 'Wayuu', 'Welsh', 'Wolaytta', 'Wolof', 'Xhosa', 'Yangben', 'Yao', 'Yapese', 'Yemba', 'Yiddish', 'Yoruba', 'Zapotec', 'Zarma', 'Zaza', 'Zeelandic', 'Zenaga', 'Zhuang', 'Zulu', 'Zuni']

countries = ["Afghanistan", "Albania", "Algeria", "American Samoa", "Angola", "Anguilla", "Antartica", "Antigua and Barbuda", "Argentina", "Armenia", "Aruba", "Ashmore and Cartier Island", "Australia", "Austria", "Azerbaijan", "Bahamas", "Bahrain", "Bangladesh", "Barbados", "Belarus", "Belgium", "Belize", "Benin", "Bermuda", "Bhutan", "Bolivia", "Bosnia and Herzegovina", "Botswana", "Brazil", "British Virgin Islands", "Brunei", "Bulgaria", "Burkina Faso", "Burma", "Burundi", "Cambodia", "Cameroon", "Canada", "Cape Verde", "Cayman Islands", "Central African Republic", "Chad", "Chile", "China", "Christmas Island", "Clipperton Island", "Cocos (Keeling) Islands", "Colombia", "Comoros", "Congo, Democratic Republic of the", "Congo, Republic of the", "Cook Islands", "Costa Rica", "Cote d'Ivoire", "Croatia", "Cuba", "Cyprus", "Czeck Republic", "Denmark", "Djibouti", "Dominica", "Dominican Republic", "Ecuador", "Egypt", "El Salvador", "Equatorial Guinea", "Eritrea", "Estonia", "Ethiopia", "Europa Island", "Falkland Islands (Islas Malvinas)", "Faroe Islands", "Fiji", "Finland", "France", "French Guiana", "French Polynesia", "French Southern and Antarctic Lands", "Gabon", "Gambia, The", "Gaza Strip", "Georgia", "Germany", "Ghana", "Gibraltar", "Glorioso Islands", "Greece", "Greenland", "Grenada", "Guadeloupe", "Guam", "Guatemala", "Guernsey", "Guinea", "Guinea-Bissau", "Guyana", "Haiti", "Heard Island and McDonald Islands", "Holy See (Vatican City)", "Honduras", "Hong Kong", "Howland Island", "Hungary", "Iceland", "India", "Indonesia", "Iran", "Iraq", "Ireland", "Ireland, Northern", "Israel", "Italy", "Jamaica", "Jan Mayen", "Japan", "Jarvis Island", "Jersey", "Johnston Atoll", "Jordan", "Juan de Nova Island", "Kazakhstan", "Kenya", "Kiribati", "Korea, North", "Korea, South", "Kuwait", "Kyrgyzstan", "Laos", "Latvia", "Lebanon", "Lesotho", "Liberia", "Libya", "Liechtenstein", "Lithuania", "Luxembourg", "Macau", "Macedonia, Former Yugoslav Republic of", "Madagascar", "Malawi", "Malaysia", "Maldives", "Mali", "Malta", "Man, Isle of", "Marshall Islands", "Martinique", "Mauritania", "Mauritius", "Mayotte", "Mexico", "Micronesia, Federated States of", "Midway Islands", "Moldova", "Monaco", "Mongolia", "Montserrat", "Morocco", "Mozambique", "Namibia", "Nauru", "Nepal", "Netherlands", "Netherlands Antilles", "New Caledonia", "New Zealand", "Nicaragua", "Niger", "Nigeria", "Niue", "Norfolk Island", "Northern Mariana Islands", "Norway", "Oman", "Pakistan", "Palau", "Panama", "Papua New Guinea", "Paraguay", "Peru", "Philippines", "Pitcaim Islands", "Poland", "Portugal", "Puerto Rico", "Qatar", "Reunion", "Romainia", "Russia", "Rwanda", "Saint Helena", "Saint Kitts and Nevis", "Saint Lucia", "Saint Pierre and Miquelon", "Saint Vincent and the Grenadines", "Samoa", "San Marino", "Sao Tome and Principe", "Saudi Arabia", "Scotland", "Senegal", "Seychelles", "Sierra Leone", "Singapore", "Slovakia", "Slovenia", "Solomon Islands", "Somalia", "South Africa", "South Georgia and South Sandwich Islands", "Spain", "Spratly Islands", "Sri Lanka", "Sudan", "Suriname", "Svalbard", "Swaziland", "Sweden", "Switzerland", "Syria", "Taiwan", "Tajikistan", "Tanzania", "Thailand", "Tobago", "Toga", "Tokelau", "Tonga", "Trinidad", "Tunisia", "Turkey", "Turkmenistan", "Tuvalu", "Uganda", "Ukraine", "United Arab Emirates", "United Kingdom", "Uruguay", "USA", "Uzbekistan", "Vanuatu", "Venezuela", "Vietnam", "Virgin Islands", "Wales", "Wallis and Futuna", "West Bank", "Western Sahara", "Yemen", "Yugoslavia", "Zambia", "Zimbabwe"]

def leet(text):
    getchar = lambda c: chars[c] if c in chars else c
    chars = {"a":"4","e":"3","l":"1","o":"0","s":"5"}
    return ''.join(getchar(c) for c in text)

s_a = ['' for x in range(253)]
s_a[0]=""
s_a[1]="Badakhshan|Badghis|Baghlan|Balkh|Bamian|Farah|Faryab|Ghazni|Ghowr|Helmand|Herat|Jowzjan|Kabol|Kandahar|Kapisa|Konar|Kondoz|Laghman|Lowgar|Nangarhar|Nimruz|Oruzgan|Paktia|Paktika|Parvan|Samangan|Sar-e Pol|Takhar|Vardak|Zabol".split("|")
s_a[2]="Berat|Bulqize|Delvine|Devoll (Bilisht)|Diber (Peshkopi)|Durres|Elbasan|Fier|Gjirokaster|Gramsh|Has (Krume)|Kavaje|Kolonje (Erseke)|Korce|Kruje|Kucove|Kukes|Kurbin|Lezhe|Librazhd|Lushnje|Malesi e Madhe (Koplik)|Mallakaster (Ballsh)|Mat (Burrel)|Mirdite (Rreshen)|Peqin|Permet|Pogradec|Puke|Sarande|Shkoder|Skrapar (Corovode)|Tepelene|Tirane (Tirana)|Tirane (Tirana)|Tropoje (Bajram Curri)|Vlore".split("|")
s_a[3]="Adrar|Ain Defla|Ain Temouchent|Alger|Annaba|Batna|Bechar|Bejaia|Biskra|Blida|Bordj Bou Arreridj|Bouira|Boumerdes|Chlef|Constantine|Djelfa|El Bayadh|El Oued|El Tarf|Ghardaia|Guelma|Illizi|Jijel|Khenchela|Laghouat|M'Sila|Mascara|Medea|Mila|Mostaganem|Naama|Oran|Ouargla|Oum el Bouaghi|Relizane|Saida|Setif|Sidi Bel Abbes|Skikda|Souk Ahras|Tamanghasset|Tebessa|Tiaret|Tindouf|Tipaza|Tissemsilt|Tizi Ouzou|Tlemcen".split("|")
s_a[4]="Eastern|Manu'a|Rose Island|Swains Island|Western".split("|")
s_a[5]="Andorra la Vella|Bengo|Benguela|Bie|Cabinda|Canillo|Cuando Cubango|Cuanza Norte|Cuanza Sul|Cunene|Encamp|Escaldes-Engordany|Huambo|Huila|La Massana|Luanda|Lunda Norte|Lunda Sul|Malanje|Moxico|Namibe|Ordino|Sant Julia de Loria|Uige|Zaire".split("|")
s_a[6]="Anguilla".split("|")
s_a[7]="Antartica".split("|")
s_a[8]="Barbuda|Redonda|Saint George|Saint John|Saint Mary|Saint Paul|Saint Peter|Saint Philip".split("|")
s_a[9]="Antartica e Islas del Atlantico Sur|Buenos Aires|Buenos Aires Capital Federal|Catamarca|Chaco|Chubut|Cordoba|Corrientes|Entre Rios|Formosa|Jujuy|La Pampa|La Rioja|Mendoza|Misiones|Neuquen|Rio Negro|Salta|San Juan|San Luis|Santa Cruz|Santa Fe|Santiago del Estero|Tierra del Fuego|Tucuman".split("|")
s_a[10]="Aragatsotn|Ararat|Armavir|Geghark'unik'|Kotayk'|Lorri|Shirak|Syunik'|Tavush|Vayots' Dzor|Yerevan".split("|")
s_a[11]="Aruba".split("|")
s_a[12]="Ashmore and Cartier Island".split("|")
s_a[13]="Australian Capital Territory|New South Wales|Northern Territory|Queensland|South Australia|Tasmania|Victoria|Western Australia".split("|")
s_a[14]="Burgenland|Kaernten|Niederoesterreich|Oberoesterreich|Salzburg|Steiermark|Tirol|Vorarlberg|Wien".split("|")
s_a[15]="Abseron Rayonu|Agcabadi Rayonu|Agdam Rayonu|Agdas Rayonu|Agstafa Rayonu|Agsu Rayonu|Ali Bayramli Sahari|Astara Rayonu|Baki Sahari|Balakan Rayonu|Barda Rayonu|Beylaqan Rayonu|Bilasuvar Rayonu|Cabrayil Rayonu|Calilabad Rayonu|Daskasan Rayonu|Davaci Rayonu|Fuzuli Rayonu|Gadabay Rayonu|Ganca Sahari|Goranboy Rayonu|Goycay Rayonu|Haciqabul Rayonu|Imisli Rayonu|Ismayilli Rayonu|Kalbacar Rayonu|Kurdamir Rayonu|Lacin Rayonu|Lankaran Rayonu|Lankaran Sahari|Lerik Rayonu|Masalli Rayonu|Mingacevir Sahari|Naftalan Sahari|Naxcivan Muxtar Respublikasi|Neftcala Rayonu|Oguz Rayonu|Qabala Rayonu|Qax Rayonu|Qazax Rayonu|Qobustan Rayonu|Quba Rayonu|Qubadli Rayonu|Qusar Rayonu|Saatli Rayonu|Sabirabad Rayonu|Saki Rayonu|Saki Sahari|Salyan Rayonu|Samaxi Rayonu|Samkir Rayonu|Samux Rayonu|Siyazan Rayonu|Sumqayit Sahari|Susa Rayonu|Susa Sahari|Tartar Rayonu|Tovuz Rayonu|Ucar Rayonu|Xacmaz Rayonu|Xankandi Sahari|Xanlar Rayonu|Xizi Rayonu|Xocali Rayonu|Xocavand Rayonu|Yardimli Rayonu|Yevlax Rayonu|Yevlax Sahari|Zangilan Rayonu|Zaqatala Rayonu|Zardab Rayonu".split("|")
s_a[16]="Acklins and Crooked Islands|Bimini|Cat Island|Exuma|Freeport|Fresh Creek|Governor's Harbour|Green Turtle Cay|Harbour Island|High Rock|Inagua|Kemps Bay|Long Island|Marsh Harbour|Mayaguana|New Providence|Nicholls Town and Berry Islands|Ragged Island|Rock Sound|San Salvador and Rum Cay|Sandy Point".split("|")
s_a[17]="Al Hadd|Al Manamah|Al Mintaqah al Gharbiyah|Al Mintaqah al Wusta|Al Mintaqah ash Shamaliyah|Al Muharraq|Ar Rifa' wa al Mintaqah al Janubiyah|Jidd Hafs|Juzur Hawar|Madinat 'Isa|Madinat Hamad|Sitrah".split("|")
s_a[18]="Barguna|Barisal|Bhola|Jhalokati|Patuakhali|Pirojpur|Bandarban|Brahmanbaria|Chandpur|Chittagong|Comilla|Cox's Bazar|Feni|Khagrachari|Lakshmipur|Noakhali|Rangamati|Dhaka|Faridpur|Gazipur|Gopalganj|Jamalpur|Kishoreganj|Madaripur|Manikganj|Munshiganj|Mymensingh|Narayanganj|Narsingdi|Netrokona|Rajbari|Shariatpur|Sherpur|Tangail|Bagerhat|Chuadanga|Jessore|Jhenaidah|Khulna|Kushtia|Magura|Meherpur|Narail|Satkhira|Bogra|Dinajpur|Gaibandha|Jaipurhat|Kurigram|Lalmonirhat|Naogaon|Natore|Nawabganj|Nilphamari|Pabna|Panchagarh|Rajshahi|Rangpur|Sirajganj|Thakurgaon|Habiganj|Maulvi bazar|Sunamganj|Sylhet".split("|")
s_a[19]="Bridgetown|Christ Church|Saint Andrew|Saint George|Saint James|Saint John|Saint Joseph|Saint Lucy|Saint Michael|Saint Peter|Saint Philip|Saint Thomas".split("|")
s_a[20]="Brestskaya (Brest)|Homyel'skaya (Homyel')|Horad Minsk|Hrodzyenskaya (Hrodna)|Mahilyowskaya (Mahilyow)|Minskaya|Vitsyebskaya (Vitsyebsk)".split("|")
s_a[21]="Antwerpen|Brabant Wallon|Brussels Capitol Region|Hainaut|Liege|Limburg|Luxembourg|Namur|Oost-Vlaanderen|Vlaams Brabant|West-Vlaanderen".split("|")
s_a[22]="Belize|Cayo|Corozal|Orange Walk|Stann Creek|Toledo".split("|")
s_a[23]="Alibori|Atakora|Atlantique|Borgou|Collines|Couffo|Donga|Littoral|Mono|Oueme|Plateau|Zou".split("|")
s_a[24]="Devonshire|Hamilton|Hamilton|Paget|Pembroke|Saint George|Saint Georges|Sandys|Smiths|Southampton|Warwick".split("|")
s_a[25]="Bumthang|Chhukha|Chirang|Daga|Geylegphug|Ha|Lhuntshi|Mongar|Paro|Pemagatsel|Punakha|Samchi|Samdrup Jongkhar|Shemgang|Tashigang|Thimphu|Tongsa|Wangdi Phodrang".split("|")
s_a[26]="Beni|Chuquisaca|Cochabamba|La Paz|Oruro|Pando|Potosi|Santa Cruz|Tarija".split("|")
s_a[27]="Federation of Bosnia and Herzegovina|Republika Srpska".split("|")
s_a[28]="Central|Chobe|Francistown|Gaborone|Ghanzi|Kgalagadi|Kgatleng|Kweneng|Lobatse|Ngamiland|North-East|Selebi-Pikwe|South-East|Southern".split("|")
s_a[29]="Acre|Alagoas|Amapa|Amazonas|Bahia|Ceara|Distrito Federal|Espirito Santo|Goias|Maranhao|Mato Grosso|Mato Grosso do Sul|Minas Gerais|Para|Paraiba|Parana|Pernambuco|Piaui|Rio de Janeiro|Rio Grande do Norte|Rio Grande do Sul|Rondonia|Roraima|Santa Catarina|Sao Paulo|Sergipe|Tocantins".split("|")
s_a[30]="Anegada|Jost Van Dyke|Tortola|Virgin Gorda".split("|")
s_a[31]="Belait|Brunei and Muara|Temburong|Tutong".split("|")
s_a[32]="Blagoevgrad|Burgas|Dobrich|Gabrovo|Khaskovo|Kurdzhali|Kyustendil|Lovech|Montana|Pazardzhik|Pernik|Pleven|Plovdiv|Razgrad|Ruse|Shumen|Silistra|Sliven|Smolyan|Sofiya|Sofiya-Grad|Stara Zagora|Turgovishte|Varna|Veliko Turnovo|Vidin|Vratsa|Yambol".split("|")
s_a[33]="Bale|Bam|Banwa|Bazega|Bougouriba|Boulgou|Boulkiemde|Comoe|Ganzourgou|Gnagna|Gourma|Houet|Ioba|Kadiogo|Kenedougou|Komandjari|Kompienga|Kossi|Koupelogo|Kouritenga|Kourweogo|Leraba|Loroum|Mouhoun|Nahouri|Namentenga|Naumbiel|Nayala|Oubritenga|Oudalan|Passore|Poni|Samentenga|Sanguie|Seno|Sissili|Soum|Sourou|Tapoa|Tuy|Yagha|Yatenga|Ziro|Zondomo|Zoundweogo".split("|")
s_a[34]="Ayeyarwady|Bago|Chin State|Kachin State|Kayah State|Kayin State|Magway|Mandalay|Mon State|Rakhine State|Sagaing|Shan State|Tanintharyi|Yangon".split("|")
s_a[35]="Bubanza|Bujumbura|Bururi|Cankuzo|Cibitoke|Gitega|Karuzi|Kayanza|Kirundo|Makamba|Muramvya|Muyinga|Mwaro|Ngozi|Rutana|Ruyigi".split("|")
s_a[36]="Banteay Mean Cheay|Batdambang|Kampong Cham|Kampong Chhnang|Kampong Spoe|Kampong Thum|Kampot|Kandal|Kaoh Kong|Keb|Kracheh|Mondol Kiri|Otdar Mean Cheay|Pailin|Phnum Penh|Pouthisat|Preah Seihanu (Sihanoukville)|Preah Vihear|Prey Veng|Rotanah Kiri|Siem Reab|Stoeng Treng|Svay Rieng|Takev".split("|")
s_a[37]="Adamaoua|Centre|Est|Extreme-Nord|Littoral|Nord|Nord-Ouest|Ouest|Sud|Sud-Ouest".split("|")
s_a[38]="Alberta|British Columbia|Manitoba|New Brunswick|Newfoundland|Northwest Territories|Nova Scotia|Nunavut|Ontario|Prince Edward Island|Quebec|Saskatchewan|Yukon Territory".split("|")
s_a[39]="Boa Vista|Brava|Maio|Mosteiros|Paul|Porto Novo|Praia|Ribeira Grande|Sal|Santa Catarina|Santa Cruz|Sao Domingos|Sao Filipe|Sao Nicolau|Sao Vicente|Tarrafal".split("|")
s_a[40]="Creek|Eastern|Midland|South Town|Spot Bay|Stake Bay|West End|Western".split("|")
s_a[41]="Bamingui-Bangoran|Bangui|Basse-Kotto|Gribingui|Haut-Mbomou|Haute-Kotto|Haute-Sangha|Kemo-Gribingui|Lobaye|Mbomou|Nana-Mambere|Ombella-Mpoko|Ouaka|Ouham|Ouham-Pende|Sangha|Vakaga".split("|")
s_a[42]="Batha|Biltine|Borkou-Ennedi-Tibesti|Chari-Baguirmi|Guera|Kanem|Lac|Logone Occidental|Logone Oriental|Mayo-Kebbi|Moyen-Chari|Ouaddai|Salamat|Tandjile".split("|")
s_a[43]="Aisen del General Carlos Ibanez del Campo|Antofagasta|Araucania|Atacama|Bio-Bio|Coquimbo|Libertador General Bernardo O'Higgins|Los Lagos|Magallanes y de la Antartica Chilena|Maule|Region Metropolitana (Santiago)|Tarapaca|Valparaiso".split("|")
s_a[44]="Anhui|Beijing|Chongqing|Fujian|Gansu|Guangdong|Guangxi|Guizhou|Hainan|Hebei|Heilongjiang|Henan|Hubei|Hunan|Jiangsu|Jiangxi|Jilin|Liaoning|Nei Mongol|Ningxia|Qinghai|Shaanxi|Shandong|Shanghai|Shanxi|Sichuan|Tianjin|Xinjiang|Xizang (Tibet)|Yunnan|Zhejiang".split("|")
s_a[45]="Christmas Island".split("|")
s_a[46]="Clipperton Island".split("|")
s_a[47]="Direction Island|Home Island|Horsburgh Island|North Keeling Island|South Island|West Island".split("|")
s_a[48]="Amazonas|Antioquia|Arauca|Atlantico|Bolivar|Boyaca|Caldas|Caqueta|Casanare|Cauca|Cesar|Choco|Cordoba|Cundinamarca|Distrito Capital de Santa Fe de Bogota|Guainia|Guaviare|Huila|La Guajira|Magdalena|Meta|Narino|Norte de Santander|Putumayo|Quindio|Risaralda|San Andres y Providencia|Santander|Sucre|Tolima|Valle del Cauca|Vaupes|Vichada".split("|")
s_a[49]="Anjouan (Nzwani)|Domoni|Fomboni|Grande Comore (Njazidja)|Moheli (Mwali)|Moroni|Moutsamoudou".split("|")
s_a[50]="Bandundu|Bas-Congo|Equateur|Kasai-Occidental|Kasai-Oriental|Katanga|Kinshasa|Maniema|Nord-Kivu|Orientale|Sud-Kivu".split("|")
s_a[51]="Bouenza|Brazzaville|Cuvette|Kouilou|Lekoumou|Likouala|Niari|Plateaux|Pool|Sangha".split("|")
s_a[52]="Aitutaki|Atiu|Avarua|Mangaia|Manihiki|Manuae|Mauke|Mitiaro|Nassau Island|Palmerston|Penrhyn|Pukapuka|Rakahanga|Rarotonga|Suwarrow|Takutea".split("|")
s_a[53]="Alajuela|Cartago|Guanacaste|Heredia|Limon|Puntarenas|San Jose".split("|")
s_a[54]="Abengourou|Abidjan|Aboisso|Adiake'|Adzope|Agboville|Agnibilekrou|Ale'pe'|Bangolo|Beoumi|Biankouma|Bocanda|Bondoukou|Bongouanou|Bouafle|Bouake|Bouna|Boundiali|Dabakala|Dabon|Daloa|Danane|Daoukro|Dimbokro|Divo|Duekoue|Ferkessedougou|Gagnoa|Grand Bassam|Grand-Lahou|Guiglo|Issia|Jacqueville|Katiola|Korhogo|Lakota|Man|Mankono|Mbahiakro|Odienne|Oume|Sakassou|San-Pedro|Sassandra|Seguela|Sinfra|Soubre|Tabou|Tanda|Tiassale|Tiebissou|Tingrela|Touba|Toulepleu|Toumodi|Vavoua|Yamoussoukro|Zuenoula".split("|")
s_a[55]="Bjelovarsko-Bilogorska Zupanija|Brodsko-Posavska Zupanija|Dubrovacko-Neretvanska Zupanija|Istarska Zupanija|Karlovacka Zupanija|Koprivnicko-Krizevacka Zupanija|Krapinsko-Zagorska Zupanija|Licko-Senjska Zupanija|Medimurska Zupanija|Osjecko-Baranjska Zupanija|Pozesko-Slavonska Zupanija|Primorsko-Goranska Zupanija|Sibensko-Kninska Zupanija|Sisacko-Moslavacka Zupanija|Splitsko-Dalmatinska Zupanija|Varazdinska Zupanija|Viroviticko-Podravska Zupanija|Vukovarsko-Srijemska Zupanija|Zadarska Zupanija|Zagreb|Zagrebacka Zupanija".split("|")
s_a[56]="Camaguey|Ciego de Avila|Cienfuegos|Ciudad de La Habana|Granma|Guantanamo|Holguin|Isla de la Juventud|La Habana|Las Tunas|Matanzas|Pinar del Rio|Sancti Spiritus|Santiago de Cuba|Villa Clara".split("|")
s_a[57]="Famagusta|Kyrenia|Larnaca|Limassol|Nicosia|Paphos".split("|")
s_a[58]="Brnensky|Budejovicky|Jihlavsky|Karlovarsky|Kralovehradecky|Liberecky|Olomoucky|Ostravsky|Pardubicky|Plzensky|Praha|Stredocesky|Ustecky|Zlinsky".split("|")
s_a[59]="Arhus|Bornholm|Fredericksberg|Frederiksborg|Fyn|Kobenhavn|Kobenhavns|Nordjylland|Ribe|Ringkobing|Roskilde|Sonderjylland|Storstrom|Vejle|Vestsjalland|Viborg".split("|")
s_a[60]="'Ali Sabih|Dikhil|Djibouti|Obock|Tadjoura".split("|")
s_a[61]="Saint Andrew|Saint David|Saint George|Saint John|Saint Joseph|Saint Luke|Saint Mark|Saint Patrick|Saint Paul|Saint Peter".split("|")
s_a[62]="Azua|Baoruco|Barahona|Dajabon|Distrito Nacional|Duarte|El Seibo|Elias Pina|Espaillat|Hato Mayor|Independencia|La Altagracia|La Romana|La Vega|Maria Trinidad Sanchez|Monsenor Nouel|Monte Cristi|Monte Plata|Pedernales|Peravia|Puerto Plata|Salcedo|Samana|San Cristobal|San Juan|San Pedro de Macoris|Sanchez Ramirez|Santiago|Santiago Rodriguez|Valverde".split("|")
s_a[63]="Azuay|Bolivar|Canar|Carchi|Chimborazo|Cotopaxi|El Oro|Esmeraldas|Galapagos|Guayas|Imbabura|Loja|Los Rios|Manabi|Morona-Santiago|Napo|Orellana|Pastaza|Pichincha|Sucumbios|Tungurahua|Zamora-Chinchipe".split("|")
s_a[64]="Ad Daqahliyah|Al Bahr al Ahmar|Al Buhayrah|Al Fayyum|Al Gharbiyah|Al Iskandariyah|Al Isma'iliyah|Al Jizah|Al Minufiyah|Al Minya|Al Qahirah|Al Qalyubiyah|Al Wadi al Jadid|As Suways|Ash Sharqiyah|Aswan|Asyut|Bani Suwayf|Bur Sa'id|Dumyat|Janub Sina'|Kafr ash Shaykh|Matruh|Qina|Shamal Sina'|Suhaj".split("|")
s_a[65]="Ahuachapan|Cabanas|Chalatenango|Cuscatlan|La Libertad|La Paz|La Union|Morazan|San Miguel|San Salvador|San Vicente|Santa Ana|Sonsonate|Usulutan".split("|")
s_a[66]="Annobon|Bioko Norte|Bioko Sur|Centro Sur|Kie-Ntem|Litoral|Wele-Nzas".split("|")
s_a[67]="Akale Guzay|Barka|Denkel|Hamasen|Sahil|Semhar|Senhit|Seraye".split("|")
s_a[68]="Harjumaa (Tallinn)|Hiiumaa (Kardla)|Ida-Virumaa (Johvi)|Jarvamaa (Paide)|Jogevamaa (Jogeva)|Laane-Virumaa (Rakvere)|Laanemaa (Haapsalu)|Parnumaa (Parnu)|Polvamaa (Polva)|Raplamaa (Rapla)|Saaremaa (Kuessaare)|Tartumaa (Tartu)|Valgamaa (Valga)|Viljandimaa (Viljandi)|Vorumaa (Voru)"
s_a[69]="Adis Abeba (Addis Ababa)|Afar|Amara|Dire Dawa|Gambela Hizboch|Hareri Hizb|Oromiya|Sumale|Tigray|YeDebub Biheroch Bihereseboch na Hizboch".split("|")
s_a[70]="Europa Island".split("|")
s_a[71]="Falkland Islands (Islas Malvinas)"
s_a[72]="Bordoy|Eysturoy|Mykines|Sandoy|Skuvoy|Streymoy|Suduroy|Tvoroyri|Vagar".split("|")
s_a[73]="Central|Eastern|Northern|Rotuma|Western".split("|")
s_a[74]="Aland|Etela-Suomen Laani|Ita-Suomen Laani|Lansi-Suomen Laani|Lappi|Oulun Laani".split("|")
s_a[75]="Alsace|Aquitaine|Auvergne|Basse-Normandie|Bourgogne|Bretagne|Centre|Champagne-Ardenne|Corse|Franche-Comte|Haute-Normandie|Ile-de-France|Languedoc-Roussillon|Limousin|Lorraine|Midi-Pyrenees|Nord-Pas-de-Calais|Pays de la Loire|Picardie|Poitou-Charentes|Provence-Alpes-Cote d'Azur|Rhone-Alpes".split("|")
s_a[76]="French Guiana".split("|")
s_a[77]="Archipel des Marquises|Archipel des Tuamotu|Archipel des Tubuai|Iles du Vent|Iles Sous-le-Vent".split("|")
s_a[78]="Adelie Land|Ile Crozet|Iles Kerguelen|Iles Saint-Paul et Amsterdam".split("|")
s_a[79]="Estuaire|Haut-Ogooue|Moyen-Ogooue|Ngounie|Nyanga|Ogooue-Ivindo|Ogooue-Lolo|Ogooue-Maritime|Woleu-Ntem".split("|")
s_a[80]="Banjul|Central River|Lower River|North Bank|Upper River|Western".split("|")
s_a[81]="Gaza Strip".split("|")
s_a[82]="Abashis|Abkhazia or Ap'khazet'is Avtonomiuri Respublika (Sokhumi)|Adigenis|Ajaria or Acharis Avtonomiuri Respublika (Bat'umi)|Akhalgoris|Akhalk'alak'is|Akhalts'ikhis|Akhmetis|Ambrolauris|Aspindzis|Baghdat'is|Bolnisis|Borjomis|Ch'khorotsqus|Ch'okhatauris|Chiat'ura|Dedop'listsqaros|Dmanisis|Dushet'is|Gardabanis|Gori|Goris|Gurjaanis|Javis|K'arelis|K'ut'aisi|Kaspis|Kharagaulis|Khashuris|Khobis|Khonis|Lagodekhis|Lanch'khut'is|Lentekhis|Marneulis|Martvilis|Mestiis|Mts'khet'is|Ninotsmindis|Onis|Ozurget'is|P'ot'i|Qazbegis|Qvarlis|Rust'avi|Sach'kheris|Sagarejos|Samtrediis|Senakis|Sighnaghis|T'bilisi|T'elavis|T'erjolis|T'et'ritsqaros|T'ianet'is|Tqibuli|Ts'ageris|Tsalenjikhis|Tsalkis|Tsqaltubo|Vanis|Zestap'onis|Zugdidi|Zugdidis".split("|")
s_a[83]="Baden-Wuerttemberg|Bayern|Berlin|Brandenburg|Bremen|Hamburg|Hessen|Mecklenburg-Vorpommern|Niedersachsen|Nordrhein-Westfalen|Rheinland-Pfalz|Saarland|Sachsen|Sachsen-Anhalt|Schleswig-Holstein|Thueringen".split("|")
s_a[84]="Ashanti|Brong-Ahafo|Central|Eastern|Greater Accra|Northern|Upper East|Upper West|Volta|Western".split("|")
s_a[85]="Gibraltar".split("|")
s_a[86]="Ile du Lys|Ile Glorieuse".split("|")
s_a[87]="Aitolia kai Akarnania|Akhaia|Argolis|Arkadhia|Arta|Attiki|Ayion Oros (Mt. Athos)|Dhodhekanisos|Drama|Evritania|Evros|Evvoia|Florina|Fokis|Fthiotis|Grevena|Ilia|Imathia|Ioannina|Irakleion|Kardhitsa|Kastoria|Kavala|Kefallinia|Kerkyra|Khalkidhiki|Khania|Khios|Kikladhes|Kilkis|Korinthia|Kozani|Lakonia|Larisa|Lasithi|Lesvos|Levkas|Magnisia|Messinia|Pella|Pieria|Preveza|Rethimni|Rodhopi|Samos|Serrai|Thesprotia|Thessaloniki|Trikala|Voiotia|Xanthi|Zakinthos".split("|")
s_a[88]="Avannaa (Nordgronland)|Kitaa (Vestgronland)|Tunu (Ostgronland)"
s_a[89]="Carriacou and Petit Martinique|Saint Andrew|Saint David|Saint George|Saint John|Saint Mark|Saint Patrick".split("|")
s_a[90]="Basse-Terre|Grande-Terre|Iles de la Petite Terre|Iles des Saintes|Marie-Galante".split("|")
s_a[91]="Guam".split("|")
s_a[92]="Alta Verapaz|Baja Verapaz|Chimaltenango|Chiquimula|El Progreso|Escuintla|Guatemala|Huehuetenango|Izabal|Jalapa|Jutiapa|Peten|Quetzaltenango|Quiche|Retalhuleu|Sacatepequez|San Marcos|Santa Rosa|Solola|Suchitepequez|Totonicapan|Zacapa".split("|")
s_a[93]="Castel|Forest|St. Andrew|St. Martin|St. Peter Port|St. Pierre du Bois|St. Sampson|St. Saviour|Torteval|Vale".split("|")
s_a[94]="Beyla|Boffa|Boke|Conakry|Coyah|Dabola|Dalaba|Dinguiraye|Dubreka|Faranah|Forecariah|Fria|Gaoual|Gueckedou|Kankan|Kerouane|Kindia|Kissidougou|Koubia|Koundara|Kouroussa|Labe|Lelouma|Lola|Macenta|Mali|Mamou|Mandiana|Nzerekore|Pita|Siguiri|Telimele|Tougue|Yomou".split("|")
s_a[95]="Bafata|Biombo|Bissau|Bolama-Bijagos|Cacheu|Gabu|Oio|Quinara|Tombali".split("|")
s_a[96]="Barima-Waini|Cuyuni-Mazaruni|Demerara-Mahaica|East Berbice-Corentyne|Essequibo Islands-West Demerara|Mahaica-Berbice|Pomeroon-Supenaam|Potaro-Siparuni|Upper Demerara-Berbice|Upper Takutu-Upper Essequibo".split("|")
s_a[97]="Artibonite|Centre|Grand'Anse|Nord|Nord-Est|Nord-Ouest|Ouest|Sud|Sud-Est".split("|")
s_a[98]="Heard Island and McDonald Islands".split("|")
s_a[99]="Holy See (Vatican City)"
s_a[100]="Atlantida|Choluteca|Colon|Comayagua|Copan|Cortes|El Paraiso|Francisco Morazan|Gracias a Dios|Intibuca|Islas de la Bahia|La Paz|Lempira|Ocotepeque|Olancho|Santa Barbara|Valle|Yoro".split("|")
s_a[101]="Hong Kong".split("|")
s_a[102]="Howland Island".split("|")
s_a[103]="Bacs-Kiskun|Baranya|Bekes|Bekescsaba|Borsod-Abauj-Zemplen|Budapest|Csongrad|Debrecen|Dunaujvaros|Eger|Fejer|Gyor|Gyor-Moson-Sopron|Hajdu-Bihar|Heves|Hodmezovasarhely|Jasz-Nagykun-Szolnok|Kaposvar|Kecskemet|Komarom-Esztergom|Miskolc|Nagykanizsa|Nograd|Nyiregyhaza|Pecs|Pest|Somogy|Sopron|Szabolcs-Szatmar-Bereg|Szeged|Szekesfehervar|Szolnok|Szombathely|Tatabanya|Tolna|Vas|Veszprem|Veszprem|Zala|Zalaegerszeg".split("|")
s_a[104]="Akranes|Akureyri|Arnessysla|Austur-Bardhastrandarsysla|Austur-Hunavatnssysla|Austur-Skaftafellssysla|Borgarfjardharsysla|Dalasysla|Eyjafjardharsysla|Gullbringusysla|Hafnarfjordhur|Husavik|Isafjordhur|Keflavik|Kjosarsysla|Kopavogur|Myrasysla|Neskaupstadhur|Nordhur-Isafjardharsysla|Nordhur-Mulasys-la|Nordhur-Thingeyjarsysla|Olafsfjordhur|Rangarvallasysla|Reykjavik|Saudharkrokur|Seydhisfjordhur|Siglufjordhur|Skagafjardharsysla|Snaefellsnes-og Hnappadalssysla|Strandasysla|Sudhur-Mulasysla|Sudhur-Thingeyjarsysla|Vesttmannaeyjar|Vestur-Bardhastrandarsysla|Vestur-Hunavatnssysla|Vestur-Isafjardharsysla|Vestur-Skaftafellssysla".split("|")
s_a[105]="Andaman and Nicobar Islands|Andhra Pradesh|Arunachal Pradesh|Assam|Bihar|Chandigarh|Chhattisgarh|Dadra and Nagar Haveli|Daman and Diu|Delhi|Goa|Gujarat|Haryana|Himachal Pradesh|Jammu and Kashmir|Jharkhand|Karnataka|Kerala|Lakshadweep|Madhya Pradesh|Maharashtra|Manipur|Meghalaya|Mizoram|Nagaland|Orissa|Pondicherry|Punjab|Rajasthan|Sikkim|Tamil Nadu|Tripura|Uttar Pradesh|Uttaranchal|West Bengal".split("|")
s_a[106]="Aceh|Bali|Banten|Bengkulu|East Timor|Gorontalo|Irian Jaya|Jakarta Raya|Jambi|Jawa Barat|Jawa Tengah|Jawa Timur|Kalimantan Barat|Kalimantan Selatan|Kalimantan Tengah|Kalimantan Timur|Kepulauan Bangka Belitung|Lampung|Maluku|Maluku Utara|Nusa Tenggara Barat|Nusa Tenggara Timur|Riau|Sulawesi Selatan|Sulawesi Tengah|Sulawesi Tenggara|Sulawesi Utara|Sumatera Barat|Sumatera Selatan|Sumatera Utara|Yogyakarta".split("|")
s_a[107]="Ardabil|Azarbayjan-e Gharbi|Azarbayjan-e Sharqi|Bushehr|Chahar Mahall va Bakhtiari|Esfahan|Fars|Gilan|Golestan|Hamadan|Hormozgan|Ilam|Kerman|Kermanshah|Khorasan|Khuzestan|Kohgiluyeh va Buyer Ahmad|Kordestan|Lorestan|Markazi|Mazandaran|Qazvin|Qom|Semnan|Sistan va Baluchestan|Tehran|Yazd|Zanjan".split("|")
s_a[108]="Al Anbar|Al Basrah|Al Muthanna|Al Qadisiyah|An Najaf|Arbil|As Sulaymaniyah|At Ta'mim|Babil|Baghdad|Dahuk|Dhi Qar|Diyala|Karbala'|Maysan|Ninawa|Salah ad Din|Wasit".split("|")
s_a[109]="Carlow|Cavan|Clare|Cork|Donegal|Dublin|Galway|Kerry|Kildare|Kilkenny|Laois|Leitrim|Limerick|Longford|Louth|Mayo|Meath|Monaghan|Offaly|Roscommon|Sligo|Tipperary|Waterford|Westmeath|Wexford|Wicklow".split("|")
s_a[110]="Antrim|Ards|Armagh|Ballymena|Ballymoney|Banbridge|Belfast|Carrickfergus|Castlereagh|Coleraine|Cookstown|Craigavon|Derry|Down|Dungannon|Fermanagh|Larne|Limavady|Lisburn|Magherafelt|Moyle|Newry and Mourne|Newtownabbey|North Down|Omagh|Strabane".split("|")
s_a[111]="Central|Haifa|Jerusalem|Northern|Southern|Tel Aviv".split("|")
s_a[112]="Abruzzo|Basilicata|Calabria|Campania|Emilia-Romagna|Friuli-Venezia Giulia|Lazio|Liguria|Lombardia|Marche|Molise|Piemonte|Puglia|Sardegna|Sicilia|Toscana|Trentino-Alto Adige|Umbria|Valle d'Aosta|Veneto".split("|")
s_a[113]="Clarendon|Hanover|Kingston|Manchester|Portland|Saint Andrew|Saint Ann|Saint Catherine|Saint Elizabeth|Saint James|Saint Mary|Saint Thomas|Trelawny|Westmoreland".split("|")
s_a[114]="Jan Mayen".split("|")
s_a[115]="Aichi|Akita|Aomori|Chiba|Ehime|Fukui|Fukuoka|Fukushima|Gifu|Gumma|Hiroshima|Hokkaido|Hyogo|Ibaraki|Ishikawa|Iwate|Kagawa|Kagoshima|Kanagawa|Kochi|Kumamoto|Kyoto|Mie|Miyagi|Miyazaki|Nagano|Nagasaki|Nara|Niigata|Oita|Okayama|Okinawa|Osaka|Saga|Saitama|Shiga|Shimane|Shizuoka|Tochigi|Tokushima|Tokyo|Tottori|Toyama|Wakayama|Yamagata|Yamaguchi|Yamanashi".split("|")
s_a[116]="Jarvis Island".split("|")
s_a[117]="Jersey".split("|")
s_a[118]="Johnston Atoll".split("|")
s_a[119]="'Amman|Ajlun|Al 'Aqabah|Al Balqa'|Al Karak|Al Mafraq|At Tafilah|Az Zarqa'|Irbid|Jarash|Ma'an|Madaba".split("|")
s_a[120]="Juan de Nova Island".split("|")
s_a[121]="Almaty|Aqmola|Aqtobe|Astana|Atyrau|Batys Qazaqstan|Bayqongyr|Mangghystau|Ongtustik Qazaqstan|Pavlodar|Qaraghandy|Qostanay|Qyzylorda|Shyghys Qazaqstan|Soltustik Qazaqstan|Zhambyl".split("|")
s_a[122]="Central|Coast|Eastern|Nairobi Area|North Eastern|Nyanza|Rift Valley|Western".split("|")
s_a[123]="Abaiang|Abemama|Aranuka|Arorae|Banaba|Banaba|Beru|Butaritari|Central Gilberts|Gilbert Islands|Kanton|Kiritimati|Kuria|Line Islands|Line Islands|Maiana|Makin|Marakei|Nikunau|Nonouti|Northern Gilberts|Onotoa|Phoenix Islands|Southern Gilberts|Tabiteuea|Tabuaeran|Tamana|Tarawa|Tarawa|Teraina".split("|")
s_a[124]="Chagang-do (Chagang Province)|Hamgyong-bukto (North Hamgyong Province)|Hamgyong-namdo (South Hamgyong Province)|Hwanghae-bukto (North Hwanghae Province)|Hwanghae-namdo (South Hwanghae Province)|Kaesong-si (Kaesong City)|Kangwon-do (Kangwon Province)|Namp'o-si (Namp'o City)|P'yongan-bukto (North P'yongan Province)|P'yongan-namdo (South P'yongan Province)|P'yongyang-si (P'yongyang City)|Yanggang-do (Yanggang Province)"
s_a[125]="Ch'ungch'ong-bukto|Ch'ungch'ong-namdo|Cheju-do|Cholla-bukto|Cholla-namdo|Inch'on-gwangyoksi|Kangwon-do|Kwangju-gwangyoksi|Kyonggi-do|Kyongsang-bukto|Kyongsang-namdo|Pusan-gwangyoksi|Soul-t'ukpyolsi|Taegu-gwangyoksi|Taejon-gwangyoksi|Ulsan-gwangyoksi".split("|")
s_a[126]="Al 'Asimah|Al Ahmadi|Al Farwaniyah|Al Jahra'|Hawalli".split("|")
s_a[127]="Batken Oblasty|Bishkek Shaary|Chuy Oblasty (Bishkek)|Jalal-Abad Oblasty|Naryn Oblasty|Osh Oblasty|Talas Oblasty|Ysyk-Kol Oblasty (Karakol)"
s_a[128]="Attapu|Bokeo|Bolikhamxai|Champasak|Houaphan|Khammouan|Louangnamtha|Louangphabang|Oudomxai|Phongsali|Salavan|Savannakhet|Viangchan|Viangchan|Xaignabouli|Xaisomboun|Xekong|Xiangkhoang".split("|")
s_a[129]="Aizkraukles Rajons|Aluksnes Rajons|Balvu Rajons|Bauskas Rajons|Cesu Rajons|Daugavpils|Daugavpils Rajons|Dobeles Rajons|Gulbenes Rajons|Jekabpils Rajons|Jelgava|Jelgavas Rajons|Jurmala|Kraslavas Rajons|Kuldigas Rajons|Leipaja|Liepajas Rajons|Limbazu Rajons|Ludzas Rajons|Madonas Rajons|Ogres Rajons|Preilu Rajons|Rezekne|Rezeknes Rajons|Riga|Rigas Rajons|Saldus Rajons|Talsu Rajons|Tukuma Rajons|Valkas Rajons|Valmieras Rajons|Ventspils|Ventspils Rajons".split("|")
s_a[130]="Beyrouth|Ech Chimal|Ej Jnoub|El Bekaa|Jabal Loubnane".split("|")
s_a[131]="Berea|Butha-Buthe|Leribe|Mafeteng|Maseru|Mohales Hoek|Mokhotlong|Qacha's Nek|Quthing|Thaba-Tseka".split("|")
s_a[132]="Bomi|Bong|Grand Bassa|Grand Cape Mount|Grand Gedeh|Grand Kru|Lofa|Margibi|Maryland|Montserrado|Nimba|River Cess|Sinoe".split("|")
s_a[133]="Ajdabiya|Al 'Aziziyah|Al Fatih|Al Jabal al Akhdar|Al Jufrah|Al Khums|Al Kufrah|An Nuqat al Khams|Ash Shati'|Awbari|Az Zawiyah|Banghazi|Darnah|Ghadamis|Gharyan|Misratah|Murzuq|Sabha|Sawfajjin|Surt|Tarabulus|Tarhunah|Tubruq|Yafran|Zlitan".split("|")
s_a[134]="Balzers|Eschen|Gamprin|Mauren|Planken|Ruggell|Schaan|Schellenberg|Triesen|Triesenberg|Vaduz".split("|")
s_a[135]="Akmenes Rajonas|Alytaus Rajonas|Alytus|Anyksciu Rajonas|Birstonas|Birzu Rajonas|Druskininkai|Ignalinos Rajonas|Jonavos Rajonas|Joniskio Rajonas|Jurbarko Rajonas|Kaisiadoriu Rajonas|Kaunas|Kauno Rajonas|Kedainiu Rajonas|Kelmes Rajonas|Klaipeda|Klaipedos Rajonas|Kretingos Rajonas|Kupiskio Rajonas|Lazdiju Rajonas|Marijampole|Marijampoles Rajonas|Mazeikiu Rajonas|Moletu Rajonas|Neringa Pakruojo Rajonas|Palanga|Panevezio Rajonas|Panevezys|Pasvalio Rajonas|Plunges Rajonas|Prienu Rajonas|Radviliskio Rajonas|Raseiniu Rajonas|Rokiskio Rajonas|Sakiu Rajonas|Salcininku Rajonas|Siauliai|Siauliu Rajonas|Silales Rajonas|Silutes Rajonas|Sirvintu Rajonas|Skuodo Rajonas|Svencioniu Rajonas|Taurages Rajonas|Telsiu Rajonas|Traku Rajonas|Ukmerges Rajonas|Utenos Rajonas|Varenos Rajonas|Vilkaviskio Rajonas|Vilniaus Rajonas|Vilnius|Zarasu Rajonas".split("|")
s_a[136]="Diekirch|Grevenmacher|Luxembourg".split("|")
s_a[137]="Macau".split("|")
s_a[138]="Aracinovo|Bac|Belcista|Berovo|Bistrica|Bitola|Blatec|Bogdanci|Bogomila|Bogovinje|Bosilovo|Brvenica|Cair (Skopje)|Capari|Caska|Cegrane|Centar (Skopje)|Centar Zupa|Cesinovo|Cucer-Sandevo|Debar|Delcevo|Delogozdi|Demir Hisar|Demir Kapija|Dobrusevo|Dolna Banjica|Dolneni|Dorce Petrov (Skopje)|Drugovo|Dzepciste|Gazi Baba (Skopje)|Gevgelija|Gostivar|Gradsko|Ilinden|Izvor|Jegunovce|Kamenjane|Karbinci|Karpos (Skopje)|Kavadarci|Kicevo|Kisela Voda (Skopje)|Klecevce|Kocani|Konce|Kondovo|Konopiste|Kosel|Kratovo|Kriva Palanka|Krivogastani|Krusevo|Kuklis|Kukurecani|Kumanovo|Labunista|Lipkovo|Lozovo|Lukovo|Makedonska Kamenica|Makedonski Brod|Mavrovi Anovi|Meseista|Miravci|Mogila|Murtino|Negotino|Negotino-Poloska|Novaci|Novo Selo|Oblesevo|Ohrid|Orasac|Orizari|Oslomej|Pehcevo|Petrovec|Plasnia|Podares|Prilep|Probistip|Radovis|Rankovce|Resen|Rosoman|Rostusa|Samokov|Saraj|Sipkovica|Sopiste|Sopotnika|Srbinovo|Star Dojran|Staravina|Staro Nagoricane|Stip|Struga|Strumica|Studenicani|Suto Orizari (Skopje)|Sveti Nikole|Tearce|Tetovo|Topolcani|Valandovo|Vasilevo|Veles|Velesta|Vevcani|Vinica|Vitoliste|Vranestica|Vrapciste|Vratnica|Vrutok|Zajas|Zelenikovo|Zileno|Zitose|Zletovo|Zrnovci".split("|")
s_a[139]="Antananarivo|Antsiranana|Fianarantsoa|Mahajanga|Toamasina|Toliara".split("|")
s_a[140]="Balaka|Blantyre|Chikwawa|Chiradzulu|Chitipa|Dedza|Dowa|Karonga|Kasungu|Likoma|Lilongwe|Machinga (Kasupe)|Mangochi|Mchinji|Mulanje|Mwanza|Mzimba|Nkhata Bay|Nkhotakota|Nsanje|Ntcheu|Ntchisi|Phalombe|Rumphi|Salima|Thyolo|Zomba".split("|")
s_a[141]="Johor|Kedah|Kelantan|Labuan|Melaka|Negeri Sembilan|Pahang|Perak|Perlis|Pulau Pinang|Sabah|Sarawak|Selangor|Terengganu|Wilayah Persekutuan".split("|")
s_a[142]="Alifu|Baa|Dhaalu|Faafu|Gaafu Alifu|Gaafu Dhaalu|Gnaviyani|Haa Alifu|Haa Dhaalu|Kaafu|Laamu|Lhaviyani|Maale|Meemu|Noonu|Raa|Seenu|Shaviyani|Thaa|Vaavu".split("|")
s_a[143]="Gao|Kayes|Kidal|Koulikoro|Mopti|Segou|Sikasso|Tombouctou".split("|")
s_a[144]="Valletta".split("|")
s_a[145]="Man, Isle of".split("|")
s_a[146]="Ailinginae|Ailinglaplap|Ailuk|Arno|Aur|Bikar|Bikini|Bokak|Ebon|Enewetak|Erikub|Jabat|Jaluit|Jemo|Kili|Kwajalein|Lae|Lib|Likiep|Majuro|Maloelap|Mejit|Mili|Namorik|Namu|Rongelap|Rongrik|Toke|Ujae|Ujelang|Utirik|Wotho|Wotje".split("|")
s_a[147]="Martinique".split("|")
s_a[148]="Adrar|Assaba|Brakna|Dakhlet Nouadhibou|Gorgol|Guidimaka|Hodh Ech Chargui|Hodh El Gharbi|Inchiri|Nouakchott|Tagant|Tiris Zemmour|Trarza".split("|")
s_a[149]="Agalega Islands|Black River|Cargados Carajos Shoals|Flacq|Grand Port|Moka|Pamplemousses|Plaines Wilhems|Port Louis|Riviere du Rempart|Rodrigues|Savanne".split("|")
s_a[150]="Mayotte".split("|")
s_a[151]="Aguascalientes|Baja California|Baja California Sur|Campeche|Chiapas|Chihuahua|Coahuila de Zaragoza|Colima|Distrito Federal|Durango|Guanajuato|Guerrero|Hidalgo|Jalisco|Mexico|Michoacan de Ocampo|Morelos|Nayarit|Nuevo Leon|Oaxaca|Puebla|Queretaro de Arteaga|Quintana Roo|San Luis Potosi|Sinaloa|Sonora|Tabasco|Tamaulipas|Tlaxcala|Veracruz-Llave|Yucatan|Zacatecas".split("|")
s_a[152]="Chuuk (Truk)|Kosrae|Pohnpei|Yap".split("|")
s_a[153]="Midway Islands".split("|")
s_a[154]="Balti|Cahul|Chisinau|Chisinau|Dubasari|Edinet|Gagauzia|Lapusna|Orhei|Soroca|Tighina|Ungheni".split("|")
s_a[155]="Fontvieille|La Condamine|Monaco-Ville|Monte-Carlo".split("|")
s_a[156]="Arhangay|Bayan-Olgiy|Bayanhongor|Bulgan|Darhan|Dornod|Dornogovi|Dundgovi|Dzavhan|Erdenet|Govi-Altay|Hentiy|Hovd|Hovsgol|Omnogovi|Ovorhangay|Selenge|Suhbaatar|Tov|Ulaanbaatar|Uvs".split("|")
s_a[157]="Saint Anthony|Saint Georges|Saint Peter's".split("|")
s_a[158]="Agadir|Al Hoceima|Azilal|Ben Slimane|Beni Mellal|Boulemane|Casablanca|Chaouen|El Jadida|El Kelaa des Srarhna|Er Rachidia|Essaouira|Fes|Figuig|Guelmim|Ifrane|Kenitra|Khemisset|Khenifra|Khouribga|Laayoune|Larache|Marrakech|Meknes|Nador|Ouarzazate|Oujda|Rabat-Sale|Safi|Settat|Sidi Kacem|Tan-Tan|Tanger|Taounate|Taroudannt|Tata|Taza|Tetouan|Tiznit".split("|")
s_a[159]="Cabo Delgado|Gaza|Inhambane|Manica|Maputo|Nampula|Niassa|Sofala|Tete|Zambezia".split("|")
s_a[160]="Caprivi|Erongo|Hardap|Karas|Khomas|Kunene|Ohangwena|Okavango|Omaheke|Omusati|Oshana|Oshikoto|Otjozondjupa".split("|")
s_a[161]="Aiwo|Anabar|Anetan|Anibare|Baiti|Boe|Buada|Denigomodu|Ewa|Ijuw|Meneng|Nibok|Uaboe|Yaren".split("|")
s_a[162]="Bagmati|Bheri|Dhawalagiri|Gandaki|Janakpur|Karnali|Kosi|Lumbini|Mahakali|Mechi|Narayani|Rapti|Sagarmatha|Seti".split("|")
s_a[163]="Drenthe|Flevoland|Friesland|Gelderland|Groningen|Limburg|Noord-Brabant|Noord-Holland|Overijssel|Utrecht|Zeeland|Zuid-Holland".split("|")
s_a[164]="Netherlands Antilles".split("|")
s_a[165]="Iles Loyaute|Nord|Sud".split("|")
s_a[166]="Akaroa|Amuri|Ashburton|Bay of Islands|Bruce|Buller|Chatham Islands|Cheviot|Clifton|Clutha|Cook|Dannevirke|Egmont|Eketahuna|Ellesmere|Eltham|Eyre|Featherston|Franklin|Golden Bay|Great Barrier Island|Grey|Hauraki Plains|Hawera|Hawke's Bay|Heathcote|Hikurangi|Hobson|Hokianga|Horowhenua|Hurunui|Hutt|Inangahua|Inglewood|Kaikoura|Kairanga|Kiwitea|Lake|Mackenzie|Malvern|Manaia|Manawatu|Mangonui|Maniototo|Marlborough|Masterton|Matamata|Mount Herbert|Ohinemuri|Opotiki|Oroua|Otamatea|Otorohanga|Oxford|Pahiatua|Paparua|Patea|Piako|Pohangina|Raglan|Rangiora|Rangitikei|Rodney|Rotorua|Runanga|Saint Kilda|Silverpeaks|Southland|Stewart Island|Stratford|Strathallan|Taranaki|Taumarunui|Taupo|Tauranga|Thames-Coromandel|Tuapeka|Vincent|Waiapu|Waiheke|Waihemo|Waikato|Waikohu|Waimairi|Waimarino|Waimate|Waimate West|Waimea|Waipa|Waipawa|Waipukurau|Wairarapa South|Wairewa|Wairoa|Waitaki|Waitomo|Waitotara|Wallace|Wanganui|Waverley|Westland|Whakatane|Whangarei|Whangaroa|Woodville".split("|")
s_a[167]="Atlantico Norte|Atlantico Sur|Boaco|Carazo|Chinandega|Chontales|Esteli|Granada|Jinotega|Leon|Madriz|Managua|Masaya|Matagalpa|Nueva Segovia|Rio San Juan|Rivas".split("|")
s_a[168]="Agadez|Diffa|Dosso|Maradi|Niamey|Tahoua|Tillaberi|Zinder".split("|")
s_a[169]="Abia|Abuja Federal Capital Territory|Adamawa|Akwa Ibom|Anambra|Bauchi|Bayelsa|Benue|Borno|Cross River|Delta|Ebonyi|Edo|Ekiti|Enugu|Gombe|Imo|Jigawa|Kaduna|Kano|Katsina|Kebbi|Kogi|Kwara|Lagos|Nassarawa|Niger|Ogun|Ondo|Osun|Oyo|Plateau|Rivers|Sokoto|Taraba|Yobe|Zamfara".split("|")
s_a[170]="Niue".split("|")
s_a[171]="Norfolk Island".split("|")
s_a[172]="Northern Islands|Rota|Saipan|Tinian".split("|")
s_a[173]="Akershus|Aust-Agder|Buskerud|Finnmark|Hedmark|Hordaland|More og Romsdal|Nord-Trondelag|Nordland|Oppland|Oslo|Ostfold|Rogaland|Sogn og Fjordane|Sor-Trondelag|Telemark|Troms|Vest-Agder|Vestfold".split("|")
s_a[174]="Ad Dakhiliyah|Al Batinah|Al Wusta|Ash Sharqiyah|Az Zahirah|Masqat|Musandam|Zufar".split("|")
s_a[175]="Balochistan|Federally Administered Tribal Areas|Islamabad Capital Territory|North-West Frontier Province|Punjab|Sindh".split("|")
s_a[176]="Aimeliik|Airai|Angaur|Hatobohei|Kayangel|Koror|Melekeok|Ngaraard|Ngarchelong|Ngardmau|Ngatpang|Ngchesar|Ngeremlengui|Ngiwal|Palau Island|Peleliu|Sonsoral|Tobi".split("|")
s_a[177]="Bocas del Toro|Chiriqui|Cocle|Colon|Darien|Herrera|Los Santos|Panama|San Blas|Veraguas".split("|")
s_a[178]="Bougainville|Central|Chimbu|East New Britain|East Sepik|Eastern Highlands|Enga|Gulf|Madang|Manus|Milne Bay|Morobe|National Capital|New Ireland|Northern|Sandaun|Southern Highlands|West New Britain|Western|Western Highlands".split("|")
s_a[179]="Alto Paraguay|Alto Parana|Amambay|Asuncion (city)|Boqueron|Caaguazu|Caazapa|Canindeyu|Central|Concepcion|Cordillera|Guaira|Itapua|Misiones|Neembucu|Paraguari|Presidente Hayes|San Pedro".split("|")
s_a[180]="Amazonas|Ancash|Apurimac|Arequipa|Ayacucho|Cajamarca|Callao|Cusco|Huancavelica|Huanuco|Ica|Junin|La Libertad|Lambayeque|Lima|Loreto|Madre de Dios|Moquegua|Pasco|Piura|Puno|San Martin|Tacna|Tumbes|Ucayali".split("|")
s_a[181]="Abra|Agusan del Norte|Agusan del Sur|Aklan|Albay|Angeles|Antique|Aurora|Bacolod|Bago|Baguio|Bais|Basilan|Basilan City|Bataan|Batanes|Batangas|Batangas City|Benguet|Bohol|Bukidnon|Bulacan|Butuan|Cabanatuan|Cadiz|Cagayan|Cagayan de Oro|Calbayog|Caloocan|Camarines Norte|Camarines Sur|Camiguin|Canlaon|Capiz|Catanduanes|Cavite|Cavite City|Cebu|Cebu City|Cotabato|Dagupan|Danao|Dapitan|Davao City Davao|Davao del Sur|Davao Oriental|Dipolog|Dumaguete|Eastern Samar|General Santos|Gingoog|Ifugao|Iligan|Ilocos Norte|Ilocos Sur|Iloilo|Iloilo City|Iriga|Isabela|Kalinga-Apayao|La Carlota|La Union|Laguna|Lanao del Norte|Lanao del Sur|Laoag|Lapu-Lapu|Legaspi|Leyte|Lipa|Lucena|Maguindanao|Mandaue|Manila|Marawi|Marinduque|Masbate|Mindoro Occidental|Mindoro Oriental|Misamis Occidental|Misamis Oriental|Mountain|Naga|Negros Occidental|Negros Oriental|North Cotabato|Northern Samar|Nueva Ecija|Nueva Vizcaya|Olongapo|Ormoc|Oroquieta|Ozamis|Pagadian|Palawan|Palayan|Pampanga|Pangasinan|Pasay|Puerto Princesa|Quezon|Quezon City|Quirino|Rizal|Romblon|Roxas|Samar|San Carlos (in Negros Occidental)|San Carlos (in Pangasinan)|San Jose|San Pablo|Silay|Siquijor|Sorsogon|South Cotabato|Southern Leyte|Sultan Kudarat|Sulu|Surigao|Surigao del Norte|Surigao del Sur|Tacloban|Tagaytay|Tagbilaran|Tangub|Tarlac|Tawitawi|Toledo|Trece Martires|Zambales|Zamboanga|Zamboanga del Norte|Zamboanga del Sur".split("|")
s_a[182]="Pitcaim Islands".split("|")
s_a[183]="Dolnoslaskie|Kujawsko-Pomorskie|Lodzkie|Lubelskie|Lubuskie|Malopolskie|Mazowieckie|Opolskie|Podkarpackie|Podlaskie|Pomorskie|Slaskie|Swietokrzyskie|Warminsko-Mazurskie|Wielkopolskie|Zachodniopomorskie".split("|")
s_a[184]="Acores (Azores)|Aveiro|Beja|Braga|Braganca|Castelo Branco|Coimbra|Evora|Faro|Guarda|Leiria|Lisboa|Madeira|Portalegre|Porto|Santarem|Setubal|Viana do Castelo|Vila Real|Viseu".split("|")
s_a[185]="Adjuntas|Aguada|Aguadilla|Aguas Buenas|Aibonito|Anasco|Arecibo|Arroyo|Barceloneta|Barranquitas|Bayamon|Cabo Rojo|Caguas|Camuy|Canovanas|Carolina|Catano|Cayey|Ceiba|Ciales|Cidra|Coamo|Comerio|Corozal|Culebra|Dorado|Fajardo|Florida|Guanica|Guayama|Guayanilla|Guaynabo|Gurabo|Hatillo|Hormigueros|Humacao|Isabela|Jayuya|Juana Diaz|Juncos|Lajas|Lares|Las Marias|Las Piedras|Loiza|Luquillo|Manati|Maricao|Maunabo|Mayaguez|Moca|Morovis|Naguabo|Naranjito|Orocovis|Patillas|Penuelas|Ponce|Quebradillas|Rincon|Rio Grande|Sabana Grande|Salinas|San German|San Juan|San Lorenzo|San Sebastian|Santa Isabel|Toa Alta|Toa Baja|Trujillo Alto|Utuado|Vega Alta|Vega Baja|Vieques|Villalba|Yabucoa|Yauco".split("|")
s_a[186]="Ad Dawhah|Al Ghuwayriyah|Al Jumayliyah|Al Khawr|Al Wakrah|Ar Rayyan|Jarayan al Batinah|Madinat ash Shamal|Umm Salal".split("|")
s_a[187]="Reunion".split("|")
s_a[188]="Alba|Arad|Arges|Bacau|Bihor|Bistrita-Nasaud|Botosani|Braila|Brasov|Bucuresti|Buzau|Calarasi|Caras-Severin|Cluj|Constanta|Covasna|Dimbovita|Dolj|Galati|Giurgiu|Gorj|Harghita|Hunedoara|Ialomita|Iasi|Maramures|Mehedinti|Mures|Neamt|Olt|Prahova|Salaj|Satu Mare|Sibiu|Suceava|Teleorman|Timis|Tulcea|Vaslui|Vilcea|Vrancea".split("|")
s_a[189]="Adygeya (Maykop)|Aginskiy Buryatskiy (Aginskoye)|Altay (Gorno-Altaysk)|Altayskiy (Barnaul)|Amurskaya (Blagoveshchensk)|Arkhangel'skaya|Astrakhanskaya|Bashkortostan (Ufa)|Belgorodskaya|Bryanskaya|Buryatiya (Ulan-Ude)|Chechnya (Groznyy)|Chelyabinskaya|Chitinskaya|Chukotskiy (Anadyr')|Chuvashiya (Cheboksary)|Dagestan (Makhachkala)|Evenkiyskiy (Tura)|Ingushetiya (Nazran')|Irkutskaya|Ivanovskaya|Kabardino-Balkariya (Nal'chik)|Kaliningradskaya|Kalmykiya (Elista)|Kaluzhskaya|Kamchatskaya (Petropavlovsk-Kamchatskiy)|Karachayevo-Cherkesiya (Cherkessk)|Kareliya (Petrozavodsk)|Kemerovskaya|Khabarovskiy|Khakasiya (Abakan)|Khanty-Mansiyskiy (Khanty-Mansiysk)|Kirovskaya|Komi (Syktyvkar)|Komi-Permyatskiy (Kudymkar)|Koryakskiy (Palana)|Kostromskaya|Krasnodarskiy|Krasnoyarskiy|Kurganskaya|Kurskaya|Leningradskaya|Lipetskaya|Magadanskaya|Mariy-El (Yoshkar-Ola)|Mordoviya (Saransk)|Moskovskaya|Moskva (Moscow)|Murmanskaya|Nenetskiy (Nar'yan-Mar)|Nizhegorodskaya|Novgorodskaya|Novosibirskaya|Omskaya|Orenburgskaya|Orlovskaya (Orel)|Penzenskaya|Permskaya|Primorskiy (Vladivostok)|Pskovskaya|Rostovskaya|Ryazanskaya|Sakha (Yakutsk)|Sakhalinskaya (Yuzhno-Sakhalinsk)|Samarskaya|Sankt-Peterburg (Saint Petersburg)|Saratovskaya|Severnaya Osetiya-Alaniya [North Ossetia] (Vladikavkaz)|Smolenskaya|Stavropol'skiy|Sverdlovskaya (Yekaterinburg)|Tambovskaya|Tatarstan (Kazan')|Taymyrskiy (Dudinka)|Tomskaya|Tul'skaya|Tverskaya|Tyumenskaya|Tyva (Kyzyl)|Udmurtiya (Izhevsk)|Ul'yanovskaya|Ust'-Ordynskiy Buryatskiy (Ust'-Ordynskiy)|Vladimirskaya|Volgogradskaya|Vologodskaya|Voronezhskaya|Yamalo-Nenetskiy (Salekhard)|Yaroslavskaya|Yevreyskaya".split("|")
s_a[190]="Butare|Byumba|Cyangugu|Gikongoro|Gisenyi|Gitarama|Kibungo|Kibuye|Kigali Rurale|Kigali-ville|Ruhengeri|Umutara".split("|")
s_a[191]="Ascension|Saint Helena|Tristan da Cunha".split("|")
s_a[192]="Christ Church Nichola Town|Saint Anne Sandy Point|Saint George Basseterre|Saint George Gingerland|Saint James Windward|Saint John Capisterre|Saint John Figtree|Saint Mary Cayon|Saint Paul Capisterre|Saint Paul Charlestown|Saint Peter Basseterre|Saint Thomas Lowland|Saint Thomas Middle Island|Trinity Palmetto Point".split("|")
s_a[193]="Anse-la-Raye|Castries|Choiseul|Dauphin|Dennery|Gros Islet|Laborie|Micoud|Praslin|Soufriere|Vieux Fort".split("|")
s_a[194]="Miquelon|Saint Pierre".split("|")
s_a[195]="Charlotte|Grenadines|Saint Andrew|Saint David|Saint George|Saint Patrick".split("|")
s_a[196]="A'ana|Aiga-i-le-Tai|Atua|Fa'asaleleaga|Gaga'emauga|Gagaifomauga|Palauli|Satupa'itea|Tuamasaga|Va'a-o-Fonoti|Vaisigano".split("|")
s_a[197]="Acquaviva|Borgo Maggiore|Chiesanuova|Domagnano|Faetano|Fiorentino|Monte Giardino|San Marino|Serravalle".split("|")
s_a[198]="Principe|Sao Tome".split("|")
s_a[199]="'Asir|Al Bahah|Al Hudud ash Shamaliyah|Al Jawf|Al Madinah|Al Qasim|Ar Riyad|Ash Sharqiyah (Eastern Province)|Ha'il|Jizan|Makkah|Najran|Tabuk".split("|")
s_a[200]="Aberdeen City|Aberdeenshire|Angus|Argyll and Bute|City of Edinburgh|Clackmannanshire|Dumfries and Galloway|Dundee City|East Ayrshire|East Dunbartonshire|East Lothian|East Renfrewshire|Eilean Siar (Western Isles)|Falkirk|Fife|Glasgow City|Highland|Inverclyde|Midlothian|Moray|North Ayrshire|North Lanarkshire|Orkney Islands|Perth and Kinross|Renfrewshire|Shetland Islands|South Ayrshire|South Lanarkshire|Stirling|The Scottish Borders|West Dunbartonshire|West Lothian".split("|")
s_a[201]="Dakar|Diourbel|Fatick|Kaolack|Kolda|Louga|Saint-Louis|Tambacounda|Thies|Ziguinchor".split("|")
s_a[202]="Anse aux Pins|Anse Boileau|Anse Etoile|Anse Louis|Anse Royale|Baie Lazare|Baie Sainte Anne|Beau Vallon|Bel Air|Bel Ombre|Cascade|Glacis|Grand' Anse (on Mahe)|Grand' Anse (on Praslin)|La Digue|La Riviere Anglaise|Mont Buxton|Mont Fleuri|Plaisance|Pointe La Rue|Port Glaud|Saint Louis|Takamaka".split("|")
s_a[203]="Eastern|Northern|Southern|Western".split("|")
s_a[204]="Singapore".split("|")
s_a[205]="Banskobystricky|Bratislavsky|Kosicky|Nitriansky|Presovsky|Trenciansky|Trnavsky|Zilinsky".split("|")
s_a[206]="Ajdovscina|Beltinci|Bled|Bohinj|Borovnica|Bovec|Brda|Brezice|Brezovica|Cankova-Tisina|Celje|Cerklje na Gorenjskem|Cerknica|Cerkno|Crensovci|Crna na Koroskem|Crnomelj|Destrnik-Trnovska Vas|Divaca|Dobrepolje|Dobrova-Horjul-Polhov Gradec|Dol pri Ljubljani|Domzale|Dornava|Dravograd|Duplek|Gorenja Vas-Poljane|Gorisnica|Gornja Radgona|Gornji Grad|Gornji Petrovci|Grosuplje|Hodos Salovci|Hrastnik|Hrpelje-Kozina|Idrija|Ig|Ilirska Bistrica|Ivancna Gorica|Izola|Jesenice|Jursinci|Kamnik|Kanal|Kidricevo|Kobarid|Kobilje|Kocevje|Komen|Koper|Kozje|Kranj|Kranjska Gora|Krsko|Kungota|Kuzma|Lasko|Lenart|Lendava|Litija|Ljubljana|Ljubno|Ljutomer|Logatec|Loska Dolina|Loski Potok|Luce|Lukovica|Majsperk|Maribor|Medvode|Menges|Metlika|Mezica|Miren-Kostanjevica|Mislinja|Moravce|Moravske Toplice|Mozirje|Murska Sobota|Muta|Naklo|Nazarje|Nova Gorica|Novo Mesto|Odranci|Ormoz|Osilnica|Pesnica|Piran|Pivka|Podcetrtek|Podvelka-Ribnica|Postojna|Preddvor|Ptuj|Puconci|Race-Fram|Radece|Radenci|Radlje ob Dravi|Radovljica|Ravne-Prevalje|Ribnica|Rogasevci|Rogaska Slatina|Rogatec|Ruse|Semic|Sencur|Sentilj|Sentjernej|Sentjur pri Celju|Sevnica|Sezana|Skocjan|Skofja Loka|Skofljica|Slovenj Gradec|Slovenska Bistrica|Slovenske Konjice|Smarje pri Jelsah|Smartno ob Paki|Sostanj|Starse|Store|Sveti Jurij|Tolmin|Trbovlje|Trebnje|Trzic|Turnisce|Velenje|Velike Lasce|Videm|Vipava|Vitanje|Vodice|Vojnik|Vrhnika|Vuzenica|Zagorje ob Savi|Zalec|Zavrc|Zelezniki|Ziri|Zrece".split("|")
s_a[207]="Bellona|Central|Choiseul (Lauru)|Guadalcanal|Honiara|Isabel|Makira|Malaita|Rennell|Temotu|Western".split("|")
s_a[208]="Awdal|Bakool|Banaadir|Bari|Bay|Galguduud|Gedo|Hiiraan|Jubbada Dhexe|Jubbada Hoose|Mudug|Nugaal|Sanaag|Shabeellaha Dhexe|Shabeellaha Hoose|Sool|Togdheer|Woqooyi Galbeed".split("|")
s_a[209]="Eastern Cape|Free State|Gauteng|KwaZulu-Natal|Mpumalanga|North-West|Northern Cape|Northern Province|Western Cape".split("|")
s_a[210]="Bird Island|Bristol Island|Clerke Rocks|Montagu Island|Saunders Island|South Georgia|Southern Thule|Traversay Islands".split("|")
s_a[211]="Andalucia|Aragon|Asturias|Baleares (Balearic Islands)|Canarias (Canary Islands)|Cantabria|Castilla y Leon|Castilla-La Mancha|Cataluna|Ceuta|Communidad Valencian|Extremadura|Galicia|Islas Chafarinas|La Rioja|Madrid|Melilla|Murcia|Navarra|Pais Vasco (Basque Country)|Penon de Alhucemas|Penon de Velez de la Gomera".split("|")
s_a[212]="Spratly Islands".split("|")
s_a[213]="Central|Eastern|North Central|North Eastern|North Western|Northern|Sabaragamuwa|Southern|Uva|Western".split("|")
s_a[214]="A'ali an Nil|Al Bahr al Ahmar|Al Buhayrat|Al Jazirah|Al Khartum|Al Qadarif|Al Wahdah|An Nil al Abyad|An Nil al Azraq|Ash Shamaliyah|Bahr al Jabal|Gharb al Istiwa'iyah|Gharb Bahr al Ghazal|Gharb Darfur|Gharb Kurdufan|Janub Darfur|Janub Kurdufan|Junqali|Kassala|Nahr an Nil|Shamal Bahr al Ghazal|Shamal Darfur|Shamal Kurdufan|Sharq al Istiwa'iyah|Sinnar|Warab".split("|")
s_a[215]="Brokopondo|Commewijne|Coronie|Marowijne|Nickerie|Para|Paramaribo|Saramacca|Sipaliwini|Wanica".split("|")
s_a[216]="Barentsoya|Bjornoya|Edgeoya|Hopen|Kvitoya|Nordaustandet|Prins Karls Forland|Spitsbergen".split("|")
s_a[217]="Hhohho|Lubombo|Manzini|Shiselweni".split("|")
s_a[218]="Blekinge|Dalarnas|Gavleborgs|Gotlands|Hallands|Jamtlands|Jonkopings|Kalmar|Kronobergs|Norrbottens|Orebro|Ostergotlands|Skane|Sodermanlands|Stockholms|Uppsala|Varmlands|Vasterbottens|Vasternorrlands|Vastmanlands|Vastra Gotalands".split("|")
s_a[219]="Aargau|Ausser-Rhoden|Basel-Landschaft|Basel-Stadt|Bern|Fribourg|Geneve|Glarus|Graubunden|Inner-Rhoden|Jura|Luzern|Neuchatel|Nidwalden|Obwalden|Sankt Gallen|Schaffhausen|Schwyz|Solothurn|Thurgau|Ticino|Uri|Valais|Vaud|Zug|Zurich".split("|")
s_a[220]="Al Hasakah|Al Ladhiqiyah|Al Qunaytirah|Ar Raqqah|As Suwayda'|Dar'a|Dayr az Zawr|Dimashq|Halab|Hamah|Hims|Idlib|Rif Dimashq|Tartus".split("|")
s_a[221]="Chang-hua|Chi-lung|Chia-i|Chia-i|Chung-hsing-hsin-ts'un|Hsin-chu|Hsin-chu|Hua-lien|I-lan|Kao-hsiung|Kao-hsiung|Miao-li|Nan-t'ou|P'eng-hu|P'ing-tung|T'ai-chung|T'ai-chung|T'ai-nan|T'ai-nan|T'ai-pei|T'ai-pei|T'ai-tung|T'ao-yuan|Yun-lin".split("|")
s_a[222]="Viloyati Khatlon|Viloyati Leninobod|Viloyati Mukhtori Kuhistoni Badakhshon".split("|")
s_a[223]="Arusha|Dar es Salaam|Dodoma|Iringa|Kagera|Kigoma|Kilimanjaro|Lindi|Mara|Mbeya|Morogoro|Mtwara|Mwanza|Pemba North|Pemba South|Pwani|Rukwa|Ruvuma|Shinyanga|Singida|Tabora|Tanga|Zanzibar Central/South|Zanzibar North|Zanzibar Urban/West".split("|")
s_a[224]="Amnat Charoen|Ang Thong|Buriram|Chachoengsao|Chai Nat|Chaiyaphum|Chanthaburi|Chiang Mai|Chiang Rai|Chon Buri|Chumphon|Kalasin|Kamphaeng Phet|Kanchanaburi|Khon Kaen|Krabi|Krung Thep Mahanakhon (Bangkok)|Lampang|Lamphun|Loei|Lop Buri|Mae Hong Son|Maha Sarakham|Mukdahan|Nakhon Nayok|Nakhon Pathom|Nakhon Phanom|Nakhon Ratchasima|Nakhon Sawan|Nakhon Si Thammarat|Nan|Narathiwat|Nong Bua Lamphu|Nong Khai|Nonthaburi|Pathum Thani|Pattani|Phangnga|Phatthalung|Phayao|Phetchabun|Phetchaburi|Phichit|Phitsanulok|Phra Nakhon Si Ayutthaya|Phrae|Phuket|Prachin Buri|Prachuap Khiri Khan|Ranong|Ratchaburi|Rayong|Roi Et|Sa Kaeo|Sakon Nakhon|Samut Prakan|Samut Sakhon|Samut Songkhram|Sara Buri|Satun|Sing Buri|Sisaket|Songkhla|Sukhothai|Suphan Buri|Surat Thani|Surin|Tak|Trang|Trat|Ubon Ratchathani|Udon Thani|Uthai Thani|Uttaradit|Yala|Yasothon".split("|")
s_a[225]="Tobago".split("|")
s_a[226]="De La Kara|Des Plateaux|Des Savanes|Du Centre|Maritime".split("|")
s_a[227]="Atafu|Fakaofo|Nukunonu".split("|")
s_a[228]="Ha'apai|Tongatapu|Vava'u".split("|")
s_a[229]="Arima|Caroni|Mayaro|Nariva|Port-of-Spain|Saint Andrew|Saint David|Saint George|Saint Patrick|San Fernando|Victoria".split("|")
s_a[230]="Ariana|Beja|Ben Arous|Bizerte|El Kef|Gabes|Gafsa|Jendouba|Kairouan|Kasserine|Kebili|Mahdia|Medenine|Monastir|Nabeul|Sfax|Sidi Bou Zid|Siliana|Sousse|Tataouine|Tozeur|Tunis|Zaghouan".split("|")
s_a[231]="Adana|Adiyaman|Afyon|Agri|Aksaray|Amasya|Ankara|Antalya|Ardahan|Artvin|Aydin|Balikesir|Bartin|Batman|Bayburt|Bilecik|Bingol|Bitlis|Bolu|Burdur|Bursa|Canakkale|Cankiri|Corum|Denizli|Diyarbakir|Duzce|Edirne|Elazig|Erzincan|Erzurum|Eskisehir|Gaziantep|Giresun|Gumushane|Hakkari|Hatay|Icel|Igdir|Isparta|Istanbul|Izmir|Kahramanmaras|Karabuk|Karaman|Kars|Kastamonu|Kayseri|Kilis|Kirikkale|Kirklareli|Kirsehir|Kocaeli|Konya|Kutahya|Malatya|Manisa|Mardin|Mugla|Mus|Nevsehir|Nigde|Ordu|Osmaniye|Rize|Sakarya|Samsun|Sanliurfa|Siirt|Sinop|Sirnak|Sivas|Tekirdag|Tokat|Trabzon|Tunceli|Usak|Van|Yalova|Yozgat|Zonguldak".split("|")
s_a[232]="Ahal Welayaty|Balkan Welayaty|Dashhowuz Welayaty|Lebap Welayaty|Mary Welayaty".split("|")
s_a[233]="Tuvalu".split("|")
s_a[234]="Adjumani|Apac|Arua|Bugiri|Bundibugyo|Bushenyi|Busia|Gulu|Hoima|Iganga|Jinja|Kabale|Kabarole|Kalangala|Kampala|Kamuli|Kapchorwa|Kasese|Katakwi|Kibale|Kiboga|Kisoro|Kitgum|Kotido|Kumi|Lira|Luwero|Masaka|Masindi|Mbale|Mbarara|Moroto|Moyo|Mpigi|Mubende|Mukono|Nakasongola|Nebbi|Ntungamo|Pallisa|Rakai|Rukungiri|Sembabule|Soroti|Tororo".split("|")
s_a[235]="Avtonomna Respublika Krym (Simferopol')|Cherkas'ka (Cherkasy)|Chernihivs'ka (Chernihiv)|Chernivets'ka (Chernivtsi)|Dnipropetrovs'ka (Dnipropetrovs'k)|Donets'ka (Donets'k)|Ivano-Frankivs'ka (Ivano-Frankivs'k)|Kharkivs'ka (Kharkiv)|Khersons'ka (Kherson)|Khmel'nyts'ka (Khmel'nyts'kyy)|Kirovohrads'ka (Kirovohrad)|Kyyiv|Kyyivs'ka (Kiev)|L'vivs'ka (L'viv)|Luhans'ka (Luhans'k)|Mykolayivs'ka (Mykolayiv)|Odes'ka (Odesa)|Poltavs'ka (Poltava)|Rivnens'ka (Rivne)|Sevastopol'|Sums'ka (Sumy)|Ternopil's'ka (Ternopil')|Vinnyts'ka (Vinnytsya)|Volyns'ka (Luts'k)|Zakarpats'ka (Uzhhorod)|Zaporiz'ka (Zaporizhzhya)|Zhytomyrs'ka (Zhytomyr)"
s_a[236]="'Ajman|Abu Zaby (Abu Dhabi)|Al Fujayrah|Ash Shariqah (Sharjah)|Dubayy (Dubai)|Ra's al Khaymah|Umm al Qaywayn".split("|")
s_a[237]="Barking and Dagenham|Barnet|Barnsley|Bath and North East Somerset|Bedfordshire|Bexley|Birmingham|Blackburn with Darwen|Blackpool|Bolton|Bournemouth|Bracknell Forest|Bradford|Brent|Brighton and Hove|Bromley|Buckinghamshire|Bury|Calderdale|Cambridgeshire|Camden|Cheshire|City of Bristol|City of Kingston upon Hull|City of London|Cornwall|Coventry|Croydon|Cumbria|Darlington|Derby|Derbyshire|Devon|Doncaster|Dorset|Dudley|Durham|Ealing|East Riding of Yorkshire|East Sussex|Enfield|Essex|Gateshead|Gloucestershire|Greenwich|Hackney|Halton|Hammersmith and Fulham|Hampshire|Haringey|Harrow|Hartlepool|Havering|Herefordshire|Hertfordshire|Hillingdon|Hounslow|Isle of Wight|Islington|Kensington and Chelsea|Kent|Kingston upon Thames|Kirklees|Knowsley|Lambeth|Lancashire|Leeds|Leicester|Leicestershire|Lewisham|Lincolnshire|Liverpool|Luton|Manchester|Medway|Merton|Middlesbrough|Milton Keynes|Newcastle upon Tyne|Newham|Norfolk|North East Lincolnshire|North Lincolnshire|North Somerset|North Tyneside|North Yorkshire|Northamptonshire|Northumberland|Nottingham|Nottinghamshire|Oldham|Oxfordshire|Peterborough|Plymouth|Poole|Portsmouth|Reading|Redbridge|Redcar and Cleveland|Richmond upon Thames|Rochdale|Rotherham|Rutland|Salford|Sandwell|Sefton|Sheffield|Shropshire|Slough|Solihull|Somerset|South Gloucestershire|South Tyneside|Southampton|Southend-on-Sea|Southwark|St. Helens|Staffordshire|Stockport|Stockton-on-Tees|Stoke-on-Trent|Suffolk|Sunderland|Surrey|Sutton|Swindon|Tameside|Telford and Wrekin|Thurrock|Torbay|Tower Hamlets|Trafford|Wakefield|Walsall|Waltham Forest|Wandsworth|Warrington|Warwickshire|West Berkshire|West Sussex|Westminster|Wigan|Wiltshire|Windsor and Maidenhead|Wirral|Wokingham|Wolverhampton|Worcestershire|York".split("|")
s_a[238]="Artigas|Canelones|Cerro Largo|Colonia|Durazno|Flores|Florida|Lavalleja|Maldonado|Montevideo|Paysandu|Rio Negro|Rivera|Rocha|Salto|San Jose|Soriano|Tacuarembo|Treinta y Tres".split("|")
s_a[239]="Alabama|Alaska|Arizona|Arkansas|California|Colorado|Connecticut|Delaware|District of Columbia|Florida|Georgia|Hawaii|Idaho|Illinois|Indiana|Iowa|Kansas|Kentucky|Louisiana|Maine|Maryland|Massachusetts|Michigan|Minnesota|Mississippi|Missouri|Montana|Nebraska|Nevada|New Hampshire|New Jersey|New Mexico|New York|North Carolina|North Dakota|Ohio|Oklahoma|Oregon|Pennsylvania|Rhode Island|South Carolina|South Dakota|Tennessee|Texas|Utah|Vermont|Virginia|Washington|West Virginia|Wisconsin|Wyoming".split("|")
s_a[240]="Andijon Wiloyati|Bukhoro Wiloyati|Farghona Wiloyati|Jizzakh Wiloyati|Khorazm Wiloyati (Urganch)|Namangan Wiloyati|Nawoiy Wiloyati|Qashqadaryo Wiloyati (Qarshi)|Qoraqalpoghiston (Nukus)|Samarqand Wiloyati|Sirdaryo Wiloyati (Guliston)|Surkhondaryo Wiloyati (Termiz)|Toshkent Shahri|Toshkent Wiloyati".split("|")
s_a[241]="Malampa|Penama|Sanma|Shefa|Tafea|Torba".split("|")
s_a[242]="Amazonas|Anzoategui|Apure|Aragua|Barinas|Bolivar|Carabobo|Cojedes|Delta Amacuro|Dependencias Federales|Distrito Federal|Falcon|Guarico|Lara|Merida|Miranda|Monagas|Nueva Esparta|Portuguesa|Sucre|Tachira|Trujillo|Vargas|Yaracuy|Zulia".split("|")
s_a[243]="An Giang|Ba Ria-Vung Tau|Bac Giang|Bac Kan|Bac Lieu|Bac Ninh|Ben Tre|Binh Dinh|Binh Duong|Binh Phuoc|Binh Thuan|Ca Mau|Can Tho|Cao Bang|Da Nang|Dac Lak|Dong Nai|Dong Thap|Gia Lai|Ha Giang|Ha Nam|Ha Noi|Ha Tay|Ha Tinh|Hai Duong|Hai Phong|Ho Chi Minh|Hoa Binh|Hung Yen|Khanh Hoa|Kien Giang|Kon Tum|Lai Chau|Lam Dong|Lang Son|Lao Cai|Long An|Nam Dinh|Nghe An|Ninh Binh|Ninh Thuan|Phu Tho|Phu Yen|Quang Binh|Quang Nam|Quang Ngai|Quang Ninh|Quang Tri|Soc Trang|Son La|Tay Ninh|Thai Binh|Thai Nguyen|Thanh Hoa|Thua Thien-Hue|Tien Giang|Tra Vinh|Tuyen Quang|Vinh Long|Vinh Phuc|Yen Bai".split("|")
s_a[244]="Saint Croix|Saint John|Saint Thomas".split("|")
s_a[245]="Blaenau Gwent|Bridgend|Caerphilly|Cardiff|Carmarthenshire|Ceredigion|Conwy|Denbighshire|Flintshire|Gwynedd|Isle of Anglesey|Merthyr Tydfil|Monmouthshire|Neath Port Talbot|Newport|Pembrokeshire|Powys|Rhondda Cynon Taff|Swansea|The Vale of Glamorgan|Torfaen|Wrexham".split("|")
s_a[246]="Alo|Sigave|Wallis".split("|")
s_a[247]="West Bank".split("|")
s_a[248]="Western Sahara".split("|")
s_a[249]="'Adan|'Ataq|Abyan|Al Bayda'|Al Hudaydah|Al Jawf|Al Mahrah|Al Mahwit|Dhamar|Hadhramawt|Hajjah|Ibb|Lahij|Ma'rib|Sa'dah|San'a'|Ta'izz".split("|")
s_a[250]="Kosovo|Montenegro|Serbia|Vojvodina".split("|")
s_a[251]="Central|Copperbelt|Eastern|Luapula|Lusaka|North-Western|Northern|Southern|Western".split("|")
s_a[252]="Bulawayo|Harare|ManicalandMashonaland Central|Mashonaland East|Mashonaland West|Masvingo|Matabeleland North|Matabeleland South|Midlands".split("|")

alphabet = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
def create_branches():
  db.raw_query("""
  CREATE TABLE project.branches
(
    country character varying(20) COLLATE pg_catalog."default" NOT NULL,
    branch_name character varying(20) COLLATE pg_catalog."default" NOT NULL,
    street_number numeric(5,0) NOT NULL,
    street_name character varying(20) COLLATE pg_catalog."default" NOT NULL,
    apt_number numeric(5,0),
    province character varying(20) COLLATE pg_catalog."default" NOT NULL,
    postal_code character varying(20) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT branches_pkey PRIMARY KEY (country)
)
   """)
  db.commit()

def create_person():
  db.raw_query("""
  CREATE TABLE project.person
(
    username character varying(20) COLLATE pg_catalog."default" NOT NULL,
    first_name character varying(20) COLLATE pg_catalog."default" NOT NULL,
    middle_name character varying(20) COLLATE pg_catalog."default",
    last_name character varying(20) COLLATE pg_catalog."default" NOT NULL,
    password character varying(20) COLLATE pg_catalog."default" NOT NULL,
    country character varying(20) COLLATE pg_catalog."default" NOT NULL,
    street_number numeric(5,0) NOT NULL,
    street_name character varying(20) COLLATE pg_catalog."default" NOT NULL,
    apt_number numeric(5,0),
    province character varying(20) COLLATE pg_catalog."default" NOT NULL,
    postal_code character varying(20) COLLATE pg_catalog."default" NOT NULL,
    date_of_birth date NOT NULL,
    CONSTRAINT person_pkey PRIMARY KEY (username),
    CONSTRAINT person_country_fkey FOREIGN KEY (country)
        REFERENCES project.branches (country) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE
)
  """)
  db.commit()


def create_users():
  db.raw_query("""
  
CREATE TABLE project.users
(
    username character varying(20) COLLATE pg_catalog."default" NOT NULL,
    join_date date NOT NULL,
    verified boolean NOT NULL,
    about text COLLATE pg_catalog."default" NOT NULL,
    languages text COLLATE pg_catalog."default" NOT NULL,
    work text COLLATE pg_catalog."default" NOT NULL,
    profile_picture character varying(20) NOT NULL,
    CONSTRAINT users_pkey PRIMARY KEY (username),
    CONSTRAINT users_username_fkey FOREIGN KEY (username)
        REFERENCES project.person (username) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
)
  """)
  db.commit()


def create_property():
  db.raw_query("""
  CREATE TABLE project.property
(
    propertyname character varying(20) COLLATE pg_catalog."default" NOT NULL,
    street_number numeric(5,0) NOT NULL,
    street_name character varying(20) COLLATE pg_catalog."default" NOT NULL,
    apt_number numeric(5,0),
    province character varying(20) COLLATE pg_catalog."default" NOT NULL,
    postal_code character varying(20) COLLATE pg_catalog."default" NOT NULL,
    rent_rate numeric(8,2) NOT NULL,
    property_type character varying(20) COLLATE pg_catalog."default" NOT NULL,
    max_guests numeric(2,0) NOT NULL,
    number_beds numeric(2,0) NOT NULL,
    number_baths numeric(2,0) NOT NULL,
    accessible boolean NOT NULL,
    pets_allowed boolean NOT NULL,
    country character varying(20) COLLATE pg_catalog."default" NOT NULL,
    hostusername character varying(20) COLLATE pg_catalog."default" NOT NULL,
    picture character varying(20) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT property_pkey PRIMARY KEY (propertyname),
    CONSTRAINT property_country_fkey FOREIGN KEY (country)
        REFERENCES project.branches (country) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE,
    CONSTRAINT property_hostusername_fkey FOREIGN KEY (hostusername)
        REFERENCES project.users (username) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT property_rent_rate_check CHECK (rent_rate > 0::numeric),
    CONSTRAINT property_type_check CHECK (property_type::text = 'entire'::text OR property_type::text = 'private'::text OR property_type::text = 'shared'::text),
    CONSTRAINT property_max_guests_check CHECK (max_guests > 0::numeric),
    CONSTRAINT property_number_beds_check CHECK (number_beds > 0::numeric),
    CONSTRAINT property_number_baths_check CHECK (number_baths > 0::numeric)
)
  """)
  db.commit()

def create_property_taken_dates():
  db.raw_query("""
  CREATE TABLE project.property_taken_dates
(
    propertyname character varying(20) COLLATE pg_catalog."default" NOT NULL,
    taken_date date NOT NULL,
    CONSTRAINT property_taken_dates_pkey PRIMARY KEY (propertyname, taken_date),
    CONSTRAINT property_taken_dates_propertyname_fkey FOREIGN KEY (propertyname)
        REFERENCES project.property (propertyname) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
)
  """)
  db.commit()

def create_property_review():
  db.raw_query("""
  CREATE TABLE project.property_review
(
    username character varying(20) COLLATE pg_catalog."default" NOT NULL,
    propertyname character varying(20) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT property_review_pkey PRIMARY KEY (username, propertyname),
    CONSTRAINT property_review_propertyname_fkey FOREIGN KEY (propertyname)
        REFERENCES project.property (propertyname) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT property_review_username_fkey FOREIGN KEY (username)
        REFERENCES project.users (username) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
) 
  """)
  db.commit()


def create_property_review_details():
  db.raw_query("""
  CREATE TABLE project.property_review_details
(
    username character varying(20) COLLATE pg_catalog."default" NOT NULL,
    propertyname character varying(20) COLLATE pg_catalog."default" NOT NULL,
    "time" timestamp without time zone NOT NULL,
    communication numeric(2,1) NOT NULL,
    value numeric(2,1) NOT NULL,
    check_in numeric(2,1) NOT NULL,
    accuracy numeric(2,1) NOT NULL,
    cleanliness numeric(2,1) NOT NULL,
    location numeric(2,1) NOT NULL,
    review_content text COLLATE pg_catalog."default",
    CONSTRAINT property_review_details_pkey PRIMARY KEY (username, propertyname, "time"),
    CONSTRAINT property_review_details_username_fkey FOREIGN KEY (propertyname, username)
        REFERENCES project.property_review (propertyname, username) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT property_review_details_communication_check CHECK (communication >= 0::numeric AND communication <= 5::numeric),
    CONSTRAINT property_review_details_value_check CHECK (value >= 0::numeric AND value <= 5::numeric),
    CONSTRAINT property_review_details_check_in_check CHECK (check_in >= 0::numeric AND check_in <= 5::numeric),
    CONSTRAINT property_review_details_accuracy_check CHECK (accuracy >= 0::numeric AND accuracy <= 5::numeric),
    CONSTRAINT property_review_details_cleanliness_check CHECK (cleanliness >= 0::numeric AND cleanliness <= 5::numeric),
    CONSTRAINT property_review_details_location_check CHECK (location >= 0::numeric AND location <= 5::numeric)
)
  """)
  db.commit()


def create_rental_agreement():
  db.raw_query("""
  CREATE TABLE project.rental_agreement
(
    rental_id character varying(20) COLLATE pg_catalog."default" NOT NULL,
    start_date date NOT NULL,
    end_date date NOT NULL,
    sign_date date,
    travelling_for_work boolean NOT NULL,
    message_to_host text COLLATE pg_catalog."default" NOT NULL,
    total_price numeric(8,2) NOT NULL,
    host_accepted boolean NOT NULL,
    propertyname character varying(20) COLLATE pg_catalog."default" NOT NULL,
    guestusername character varying(20) COLLATE pg_catalog."default" NOT NULL,
    hostusername character varying(20) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT rental_agreement_pkey PRIMARY KEY (rental_id),
    CONSTRAINT rental_agreement_guestusername_fkey FOREIGN KEY (guestusername)
        REFERENCES project.users (username) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE SET NULL,
    CONSTRAINT rental_agreement_hostusername_fkey FOREIGN KEY (hostusername)
        REFERENCES project.users (username) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE SET NULL,
    CONSTRAINT rental_agreement_propertyname_fkey FOREIGN KEY (propertyname)
        REFERENCES project.property (propertyname) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE SET NULL,
    CONSTRAINT rental_agreement_total_price_check CHECK (total_price > 0::numeric)
)
  """)
  db.commit()

def create_employees():
  db.raw_query("""
CREATE TABLE project.employees
(
    username character varying(20) COLLATE pg_catalog."default" NOT NULL,
    title text COLLATE pg_catalog."default" NOT NULL,
    salary numeric(8,2) NOT NULL,
    country character varying(20) COLLATE pg_catalog."default" NOT NULL,
    managerusername character varying(20) COLLATE pg_catalog."default",
    CONSTRAINT employees_pkey PRIMARY KEY (username),
    CONSTRAINT employees_country_fkey FOREIGN KEY (country)
        REFERENCES project.branches (country) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE,
    CONSTRAINT employees_username_fkey FOREIGN KEY (username)
        REFERENCES project.person (username) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT employees_managerusername_fkey FOREIGN KEY (managerusername)
        REFERENCES project.employees (username) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE SET NULL,
    CONSTRAINT employees_salary_check CHECK (salary > 0::numeric)
)
  """)
  db.commit()

def create_admins():
  db.raw_query("""
  CREATE TABLE project.admins
(
    username character varying(20) COLLATE pg_catalog."default",
    CONSTRAINT admins_pkey PRIMARY KEY (username),
    CONSTRAINT admins_username2_fkey FOREIGN KEY (username)
        REFERENCES project.employees (username) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT admins_username_fkey FOREIGN KEY (username)
        REFERENCES project.person (username) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
)
  """)
  db.commit()

def create_works_at():
  db.raw_query("""
  CREATE TABLE project.works_at
(
    employeeusername character varying(20) COLLATE pg_catalog."default" NOT NULL,
    propertyname character varying(20) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT works_at_pkey PRIMARY KEY (employeeusername, propertyname),
    CONSTRAINT works_at_employeeusername_fkey FOREIGN KEY (employeeusername)
        REFERENCES project.employees (username) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT works_at_propertyname_fkey FOREIGN KEY (propertyname)
        REFERENCES project.property (propertyname) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
)
  """)
  db.commit()


def create_conversation():
  db.raw_query("""
  CREATE TABLE project.conversation
(
    senderusername character varying(20) COLLATE pg_catalog."default" NOT NULL,
    receiverusername character varying(20) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT conversation_pkey PRIMARY KEY (senderusername, receiverusername),
    CONSTRAINT conversation_receiverusername_fkey FOREIGN KEY (receiverusername)
        REFERENCES project.person (username) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT conversation_senderusername_fkey FOREIGN KEY (senderusername)
        REFERENCES project.person (username) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
)
  """)
  db.commit()


def create_conversation_messages():
  db.raw_query("""
CREATE TABLE project.conversation_messages
(
    senderusername character varying(20) COLLATE pg_catalog."default" NOT NULL,
    receiverusername character varying(20) COLLATE pg_catalog."default" NOT NULL,
    "time" timestamp without time zone NOT NULL,
    message_content text COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT conversation_messages_pkey PRIMARY KEY (senderusername, receiverusername, "time"),
    CONSTRAINT conversation_messages_senderusername_fkey FOREIGN KEY (receiverusername, senderusername)
        REFERENCES project.conversation (receiverusername, senderusername) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
)
  """)
  db.commit()

def create_payment():
  db.raw_query("""
  CREATE TABLE project.payment
(
    payment_id character varying(20) COLLATE pg_catalog."default" NOT NULL,
    is_deposit boolean NOT NULL,
    amount numeric(8,2) NOT NULL,
    status character varying(20) COLLATE pg_catalog."default" NOT NULL,
    rental_id character varying(20) COLLATE pg_catalog."default" NOT NULL,
    guestusername character varying(20) COLLATE pg_catalog."default" NOT NULL,
    hostusername character varying(20) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT payment_pkey PRIMARY KEY (payment_id),
    CONSTRAINT payment_guestusername_fkey FOREIGN KEY (guestusername)
        REFERENCES project.users (username) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE SET NULL,
    CONSTRAINT payment_hostusername_fkey FOREIGN KEY (hostusername)
        REFERENCES project.users (username) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE SET NULL,
    CONSTRAINT payment_rental_id_fkey FOREIGN KEY (rental_id)
        REFERENCES project.rental_agreement (rental_id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE SET NULL,
    CONSTRAINT payment_amount_check CHECK (amount > 0::numeric),
    CONSTRAINT payment_status_check CHECK (status::text = 'approved'::text OR status::text = 'pending'::text)
)
  """)
  db.commit()

def create_payment_method():
  db.raw_query("""
  CREATE TABLE project.payment_method
(
    username character varying(20) COLLATE pg_catalog."default" NOT NULL,
    card_type character varying(20) COLLATE pg_catalog."default" NOT NULL,
    first_name character varying(20) COLLATE pg_catalog."default" NOT NULL,
    last_name character varying(20) COLLATE pg_catalog."default" NOT NULL,
    card_number character varying(20) COLLATE pg_catalog."default" NOT NULL,
    card_expiration date NOT NULL,
    cvv character varying(3) COLLATE pg_catalog."default" NOT NULL,
    billing_country character varying(20) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT payment_method_pkey PRIMARY KEY (username),
    CONSTRAINT payment_method_username_fkey FOREIGN KEY (username)
        REFERENCES project.users (username) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT payment_method_billing_country_fkey FOREIGN KEY (billing_country)
        REFERENCES project.branches (country) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE,
    CONSTRAINT card_type CHECK (card_type::text = 'visa'::text OR card_type::text = 'mastercard'::text)
)
  """)
  db.commit()

def create_payout_method():
  db.raw_query("""
  CREATE TABLE project.payout_method
(
    username character varying(20) COLLATE pg_catalog."default" NOT NULL,
    paypal_address character varying(20) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT payout_method_pkey PRIMARY KEY (username),
    CONSTRAINT payout_method_username_fkey FOREIGN KEY (username)
        REFERENCES project.person (username) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
)
  """)
  db.commit()


def create_person_email_address():
  db.raw_query("""
  CREATE TABLE project.person_email_address
(
    username character varying(20) COLLATE pg_catalog."default" NOT NULL,
    email_address character varying(20) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT person_email_address_pkey PRIMARY KEY (username, email_address),
    CONSTRAINT person_email_address_username_fkey FOREIGN KEY (username)
        REFERENCES project.person (username) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
)
  """)
  db.commit()

def create_person_phone_number():
  db.raw_query("""
  CREATE TABLE project.person_phone_number
(
    username character varying(20) COLLATE pg_catalog."default" NOT NULL,
    phone_number character varying(20) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT person_phone_number_pkey PRIMARY KEY (username, phone_number),
    CONSTRAINT person_phone_number_username_fkey FOREIGN KEY (username)
        REFERENCES project.person (username) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
)
  """)
  db.commit()

def create_user_review():
  db.raw_query("""
  CREATE TABLE project.user_review
(
    reviewerusername character varying(20) COLLATE pg_catalog."default" NOT NULL,
    revieweeusername character varying(20) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT user_review_pkey PRIMARY KEY (reviewerusername, revieweeusername),
    CONSTRAINT user_review_revieweeusername_fkey FOREIGN KEY (revieweeusername)
        REFERENCES project.users (username) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT user_review_reviewerusername_fkey FOREIGN KEY (reviewerusername)
        REFERENCES project.users (username) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT user_review_check CHECK (revieweeusername::text <> reviewerusername::text)
)
  """)
  db.commit()

def create_user_review_details():
  db.raw_query("""
CREATE TABLE project.user_review_details
(
    reviewerusername character varying(20) COLLATE pg_catalog."default" NOT NULL,
    revieweeusername character varying(20) COLLATE pg_catalog."default" NOT NULL,
    "time" timestamp without time zone NOT NULL,
    review_content text COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT user_review_details_pkey PRIMARY KEY (reviewerusername, revieweeusername, "time"),
    CONSTRAINT user_review_details_reviewerusername_fkey FOREIGN KEY (revieweeusername, reviewerusername)
        REFERENCES project.user_review (revieweeusername, reviewerusername) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT user_review_details_check CHECK (revieweeusername::text <> reviewerusername::text)
)
  """)
  db.commit()

def create_all_tables():
  create_branches()
  create_person()
  create_users()
  create_property()
  create_property_taken_dates()
  create_property_review()
  create_property_review_details()
  create_rental_agreement()
  create_employees()
  create_admins()
  create_works_at()
  create_conversation()
  create_conversation_messages()
  create_payment()
  create_payment_method()
  create_payout_method()
  create_person_email_address()
  create_person_phone_number()
  create_user_review()
  create_user_review_details()

def insert_branches():
  for i in range(len(countries)):
    country = countries[i].replace("'", "-")
    if len(country) > 20:
      continue
    province_choices = s_a[i + 1]
    province = random.choice(province_choices).replace("'", "-")
    while len(province) > 20:
      province = random.choice(province_choices).replace("'", "-")
    
    street_number = random.randint(1, 999)
    street_name = fake.street_name().replace("'", "-")
    while len(street_name) > 20:
      street_name = fake.street_name().replace("'", "-")

    #apt_number can be null
    apt_numbers = [x for x in range(1, 999)]
    apt_numbers.append("NaN")
    apt_number = random.choice(apt_numbers)

    branch_number = random.randint(1000, 9999)
    branch_name = "Branch " + str(branch_number)

    postal_code = ""
    for i in range(3):
      postal_code += random.choice(alphabet)
      postal_code += str(random.randint(1, 9))
    
    db.raw_query(f"""INSERT INTO BRANCHES (country, branch_name, street_number, street_name, apt_number, province, postal_code) VALUES ('{country}', '{branch_name}', '{street_number}', '{street_name}', '{apt_number}', '{province}', '{postal_code}')""")

  db.commit()

#inserts data into person, users, person_phone_number, person_email_address, employees, admins, properties, payment_method, payout_method
def create_alot(generation_size):
  if generation_size == 'small':
    generation_size = 5
  elif generation_size == 'medium':
    generation_size = 10
  elif generation_size == 'large':
    generation_size = 25
    
  try:
    #making person
    for i in range(len(countries)):
    #reduce_data = 5
    #for i in range(reduce_data):
      ##### reduce number of countries to test ######
      completion = (i/(len(countries)))*100
      print("generating users, properties, employees, emails, pictures, etc.... " + str(round(completion, 2)) + "% done")
      #if we move the next 3 statements inside next for loop it breaks weirdly... but why? 
      country = countries[i].replace("'", "-")
      if len(country) > 20:
          continue
      employees_in_country = []
      #generation size is # of people per country
      for person_from_country in range(generation_size):
        province_choices = s_a[i + 1]
        province = random.choice(province_choices).replace("'", "-")
        while len(province) > 20:
          province = random.choice(province_choices).replace("'", "-")

        street_number = random.randint(1, 999)
        street_name = fake.street_name().replace("'", "-")
        while len(street_name) > 20:
          street_name = fake.street_name().replace("'", "-")

        #apt_number can be null
        apt_numbers = [x for x in range(1, 999)]
        apt_numbers.append("NaN")
        apt_number = random.choice(apt_numbers)

        postal_code = ""
        for i in range(3):
          postal_code += random.choice(alphabet)
          postal_code += str(random.randint(1, 9))

        random_int = random.randint(1,9)
        if random_int == 1:
          username = generate_username()[0] + random.choice(alphabet) + str(random.randint(1, 999))
          random_int = random.randint(1,3)
          if random_int == 1:
            username += random.choice(alphabet)
          elif random_int == 2:
            username = leet(username)

        elif random_int == 2:
          username = fake.name() + generate_username()[0] + random.choice(alphabet) + str(random.randint(1, 999))
          random_int = random.randint(1,3)
          if random_int == 1:
            username += random.choice(alphabet)
          elif random_int == 2:
            username = leet(username)
          
        elif random_int == 3:
          username = fake.company() + str(random.randint(1, 999)) + fake.name()
          random_int = random.randint(1,3)
          if random_int == 1:
            username += random.choice(alphabet)
          elif random_int == 2:
            username = leet(username)

        elif random_int == 4:
          username = generate_username()[0] + str(random.randint(1, 9999))
          random_int = random.randint(1,3)
          if random_int == 1:
            username += random.choice(alphabet)
          elif random_int == 2:
            username = leet(username)
        
        elif random_int == 5:
          username = fake.name() + fake.name() + str(random.randint(1, 9999))
          random_int = random.randint(1,3)
          if random_int == 1:
            username += random.choice(alphabet)
          elif random_int == 2:
            username = leet(username)
        
        elif random_int == 6:
          username = fake.word() + fake.word() + str(random.randint(1, 9999))
          random_int = random.randint(1,3)
          if random_int == 1:
            username += random.choice(alphabet)
          elif random_int == 2:
            username = leet(username)
        
        elif random_int == 7:
          username = fake.word() + generate_username()[0] + str(random.randint(1, 9999))
          random_int = random.randint(1,3)
          if random_int == 1:
            username += random.choice(alphabet)
          elif random_int == 2:
            username = leet(username)
        
        elif random_int == 8:
          username = fake.word() + fake.company() + random.choice(alphabet) + str(random.randint(1, 9999))
          random_int = random.randint(1,3)
          if random_int == 1:
            username += random.choice(alphabet)
          elif random_int == 2:
            username = leet(username)

        else:
          username = fake.street_name() + fake.word() + str(random.randint(1, 9999))
          random_int = random.randint(1,3)
          if random_int == 1:
            username += random.choice(alphabet)
          elif random_int == 2:
            username = leet(username)

        while len(username) > 20:
          random_int = random.randint(1,9)
          if random_int == 1:
            username = generate_username()[0] + random.choice(alphabet) + str(random.randint(1, 999))
            random_int = random.randint(1,3)
            if random_int == 1:
              username += random.choice(alphabet)
            elif random_int == 2:
              username = leet(username)

          elif random_int == 2:
            username = fake.name() + generate_username()[0] + random.choice(alphabet) + str(random.randint(1, 999))
            random_int = random.randint(1,3)
            if random_int == 1:
              username += random.choice(alphabet)
            elif random_int == 2:
              username = leet(username)

          elif random_int == 3:
            username = fake.company() + str(random.randint(1, 999)) + fake.name()
            random_int = random.randint(1,3)
            if random_int == 1:
              username += random.choice(alphabet)
            elif random_int == 2:
              username = leet(username)


          elif random_int == 4:
            username = generate_username()[0] + str(random.randint(1, 9999))
            random_int = random.randint(1,3)
            if random_int == 1:
              username += random.choice(alphabet)
            elif random_int == 2:
              username = leet(username)
          
          elif random_int == 5:
            username = fake.name() + fake.name() + str(random.randint(1, 9999))
            random_int = random.randint(1,3)
            if random_int == 1:
              username += random.choice(alphabet)
            elif random_int == 2:
              username = leet(username)
          
          elif random_int == 6:
            username = fake.word() + fake.word() + str(random.randint(1, 9999))
            random_int = random.randint(1,3)
            if random_int == 1:
              username += random.choice(alphabet)
            elif random_int == 2:
              username = leet(username)
          
          elif random_int == 7:
            username = fake.word() + generate_username()[0] + str(random.randint(1, 9999))
            random_int = random.randint(1,3)
            if random_int == 1:
              username += random.choice(alphabet)
            elif random_int == 2:
              username = leet(username)
          
          elif random_int == 8:
            username = fake.word() + fake.company() + random.choice(alphabet) + str(random.randint(1, 9999))
            random_int = random.randint(1,3)
            if random_int == 1:
              username += random.choice(alphabet)
            elif random_int == 2:
              username = leet(username)

          else:
            username = fake.street_name() + fake.word() + str(random.randint(1, 9999))
            random_int = random.randint(1,3)
            if random_int == 1:
              username += random.choice(alphabet)
            elif random_int == 2:
              username = leet(username)

        
        username = username.replace(' ', '-')
        first_name = fake.first_name()
        middle_name = random.choice(['', fake.first_name()])
        last_name = fake.last_name()
        password = fake.password()
        date_of_birth = fake.date()
        db.raw_query(f"""INSERT INTO PERSON (username, first_name, middle_name, last_name, password, country, street_number, street_name, apt_number, province, postal_code, date_of_birth) VALUES ('{username}', '{first_name}', '{middle_name}', '{last_name}', '{password}', '{country}', '{street_number}', '{street_name}', '{apt_number}', '{province}', '{postal_code}', '{date_of_birth}')""")

        #add to users now
        join_date = fake.date_between(start_date='-60d', end_date='today').strftime('%Y-%m-%d')
        verified = random.choice(['true', 'false'])
        about = fake.text(100)
        languages = ""
        number_languages = random.randint(1,3)
        languages += "English"
        number_languages -= 1
        if number_languages == 0:
          pass
        else:
          languages += ", "
        while number_languages > 0:
          languages += (random.choice(language_choices))
          number_languages -= 1
          if number_languages == 0:
            pass
          else:
            languages += ", "
          
        r = requests.get('https://fakedata.dev/users/v1/get_random_user')
        data = r.json()
        work = data['jobTitle']
        picture = data['photoUrl']
        random_name = secrets.token_hex(6)
        urllib.request.urlretrieve(picture, "../static/images/" + random_name + ".png")
        profile_picture = random_name + ".png"

        db.raw_query(f"""INSERT INTO users (username, join_date, verified, about, languages, work, profile_picture) VALUES ('{username}', '{join_date}', '{verified}', '{about}', '{languages}', '{work}', '{profile_picture}')""")

        #email 
        email_address = fake.email()
        while len(email_address) > 20:
          email_address = fake.email()

        db.raw_query(f"""INSERT INTO person_email_address (username, email_address) VALUES ('{username}', '{email_address}')""")

        #phone
        phone_number = fake.phone_number().replace('.', '-').split('x')[0]
        while len(phone_number) > 20:
          phone_number = fake.phone_number().replace('.', '-').split('x')[0]

        db.raw_query(f"""INSERT INTO person_phone_number (username, phone_number) VALUES ('{username}', '{phone_number}')""")

        #employees
        #roll for if this person should be an employee
        random_int = random.randint(1,10)
        if random_int == 1:
          work = "AirBnB Employee"
          salary = random.choice(salaries)
          #roll for if they should have a manager (they must not if len(employee_dict[country]) == 0 )
          random_int = random.randint(1,10)
          if ((len(employees_in_country) == 0) or (random_int == 1)):
            managerusername = username
            title = "Branch Manager"
          else:
            managerusername = random.choice(employees_in_country)
            title = random.choice(titles)
          employees_in_country.append(username)
          
          #roll for if this person should be an admin 
          random_int = random.randint(1,5)
          is_admin = False
          if ((random_int == 1) and (title != "Branch Manager")):
            is_admin = True
            title = "Admin"

          db.raw_query(f"""INSERT INTO employees (username, title, salary, country, managerusername) VALUES ('{username}', '{title}', '{salary}', '{country}', '{managerusername}')""")
          db.raw_query(f""" UPDATE users SET work='{work}' WHERE username='{username}' """)

          #admins 
          if is_admin:
            db.raw_query(f"""INSERT INTO admins (username) VALUES ('{username}')""")
        
        ########### property creation ###########
        number_properties = random.randint(1,3)
        if work != "AirBnB Employee":
          for create_propety in range(number_properties):
            random_int = random.randint(1,15)
            if random_int == 1:
              propertyname = fake.company() + random.choice(["!", "NEW", "new", "(new)", "", 'Getaway!']) + str(random.randint(1, 999)) + random.choice(alphabet)
              random_int = random.randint(1,3)
              if random_int == 1:
                propertyname = leet(propertyname)
              elif random_int == 2:
                propertyname = leet(propertyname[:10] + fake.name())
              
            elif random_int == 2:
              propertyname =  str(random.randint(1, 999)) + random.choice(alphabet) + fake.company() + str(random.randint(1, 999)) + random.choice(alphabet)
              random_int = random.randint(1,3)
              if random_int == 1:
                propertyname = leet(propertyname)
              elif random_int == 2:
                propertyname = leet(propertyname[:10] + fake.name())

            elif random_int == 3:
              propertyname = random.choice(alphabet) + random.choice(["Stay With ", "The ", "(new)", "*NEW*"]) + fake.company() + str(random.randint(1, 999))
              random_int = random.randint(1,3)
              if random_int == 1:
                propertyname = leet(propertyname)
              elif random_int == 2:
                propertyname = leet(propertyname[:10] + fake.name())

            elif random_int == 4:
              propertyname = str(random.randint(1, 999)) + fake.street_name() + random.choice(["!", "NEW", "new", "(new)", "", 'Getaway!']) + random.choice(alphabet)
              random_int = random.randint(1,3)
              if random_int == 1:
                propertyname = leet(propertyname)
              elif random_int == 2:
                propertyname = leet(propertyname[:10] + fake.name())

            elif random_int == 5:
              propertyname = random.choice(alphabet) + random.choice(["Stay With ", "The ", "(new)", "*NEW*"]) + fake.street_name() + str(random.randint(1, 999))
              random_int = random.randint(1,3)
              if random_int == 1:
                propertyname = leet(propertyname)
              elif random_int == 2:
                propertyname = leet(propertyname[:10] + fake.name())

            elif random_int == 6:
              propertyname = str(random.randint(1, 999)) + fake.street_name() + random.choice(alphabet) + random.choice(["!", "NEW", "new", "(new)", "", 'Getaway!'])
              random_int = random.randint(1,3)
              if random_int == 1:
                propertyname = leet(propertyname)
              elif random_int == 2:
                propertyname = leet(propertyname[:10] + fake.name())

            elif random_int == 7:
              propertyname = fake.company() + fake.street_name() + str(random.randint(1, 999)) + random.choice(alphabet)
              random_int = random.randint(1,3)
              if random_int == 1:
                propertyname = leet(propertyname)
              elif random_int == 2:
                propertyname = leet(propertyname[:10] + fake.name())

            elif random_int == 8:
              propertyname = random.choice(alphabet) + str(random.randint(1, 999)) + fake.company() + fake.street_name()
              random_int = random.randint(1,3)
              if random_int == 1:
                propertyname = leet(propertyname)
              elif random_int == 2:
                propertyname = leet(propertyname[:10] + fake.name())

            elif random_int == 9:
              propertyname = fake.street_name() + fake.street_name() + str(random.randint(1, 999)) + random.choice(alphabet)
              random_int = random.randint(1,3)
              if random_int == 1:
                propertyname = leet(propertyname)
              elif random_int == 2:
                propertyname = leet(propertyname[:10] + fake.name())

            elif random_int == 10:
              propertyname = fake.company() + str(random.randint(1, 999)) + fake.street_name() + random.choice(alphabet)
              random_int = random.randint(1,3)
              if random_int == 1:
                propertyname = leet(propertyname)
              elif random_int == 2:
                propertyname = leet(propertyname[:10] + fake.name())

            elif random_int == 11:
              propertyname = random.choice(alphabet) + str(random.randint(1, 999)) + fake.street_name() + fake.company() + random.choice(["!", "NEW", "new", "(new)", "", 'Getaway!'])
              random_int = random.randint(1,3)
              if random_int == 1:
                propertyname = leet(propertyname)
              elif random_int == 2:
                propertyname = leet(propertyname[:10] + fake.name())

            elif random_int == 12:
              propertyname = fake.first_name() + str(random.randint(1, 999)) + random.choice(alphabet) + random.choice(["Best", "Renovated ", "(new)", "*NEW*"])
              random_int = random.randint(1,3)
              if random_int == 1:
                propertyname = leet(propertyname)
              elif random_int == 2:
                propertyname = leet(propertyname[:10] + fake.name())

            elif random_int == 13:
              propertyname = random.choice(["Best", "Renovated ", "(new)", "*NEW*"]) + fake.name() + str(random.randint(1, 999)) + random.choice(alphabet)
              random_int = random.randint(1,3)
              if random_int == 1:
                propertyname = leet(propertyname)
              elif random_int == 2:
                propertyname = leet(propertyname[:10] + fake.name())

            elif random_int == 14:
              propertyname = random.choice(alphabet) + str(random.randint(1, 999)) + fake.street_name() + fake.company() + fake.name()
              random_int = random.randint(1,3)
              if random_int == 1:
                propertyname = leet(propertyname)
              elif random_int == 2:
                propertyname = leet(propertyname[:10] + fake.name())

            else:
              propertyname = random.choice(["Stay With ", "The ", "(new)", "*NEW*"]) + fake.street_name() + random.choice(alphabet) + str(random.randint(1, 999)) + fake.company()
              random_int = random.randint(1,3)
              if random_int == 1:
                propertyname = leet(propertyname)
              elif random_int == 2:
                propertyname = leet(propertyname[:10] + fake.name())


            while len(propertyname) > 20:
              random_int = random.randint(1,15)
              if random_int == 1:
                propertyname = fake.company() + random.choice(["!", "NEW", "new", "(new)", "", 'Getaway!']) + str(random.randint(1, 999)) + random.choice(alphabet)
                random_int = random.randint(1,3)
                if random_int == 1:
                  propertyname = leet(propertyname)
                elif random_int == 2:
                  propertyname = leet(propertyname[:10] + fake.name())

              elif random_int == 2:
                propertyname =  str(random.randint(1, 999)) + random.choice(alphabet) + fake.company() + str(random.randint(1, 999)) + random.choice(alphabet)
                random_int = random.randint(1,3)
                if random_int == 1:
                  propertyname = leet(propertyname)
                elif random_int == 2:
                  propertyname = leet(propertyname[:10] + fake.name())

              elif random_int == 3:
                propertyname = random.choice(alphabet) + random.choice(["Stay With ", "The ", "(new)", "*NEW*"]) + fake.company() + str(random.randint(1, 999))
                random_int = random.randint(1,3)
                if random_int == 1:
                  propertyname = leet(propertyname)
                elif random_int == 2:
                  propertyname = leet(propertyname[:10] + fake.name())

              elif random_int == 4:
                propertyname = str(random.randint(1, 999)) + fake.street_name() + random.choice(["!", "NEW", "new", "(new)", "", 'Getaway!']) + random.choice(alphabet)
                random_int = random.randint(1,3)
                if random_int == 1:
                  propertyname = leet(propertyname)
                elif random_int == 2:
                  propertyname = leet(propertyname[:10] + fake.name())

              elif random_int == 5:
                propertyname = random.choice(alphabet) + random.choice(["Stay With ", "The ", "(new)", "*NEW*"]) + fake.street_name() + str(random.randint(1, 999))
                random_int = random.randint(1,3)
                if random_int == 1:
                  propertyname = leet(propertyname)
                elif random_int == 2:
                  propertyname = leet(propertyname[:10] + fake.name())

              elif random_int == 6:
                propertyname = str(random.randint(1, 999)) + fake.street_name() + random.choice(alphabet) + random.choice(["!", "NEW", "new", "(new)", "", 'Getaway!'])
                random_int = random.randint(1,3)
                if random_int == 1:
                  propertyname = leet(propertyname)
                elif random_int == 2:
                  propertyname = leet(propertyname[:10] + fake.name())

              elif random_int == 7:
                propertyname = fake.company() + fake.street_name() + str(random.randint(1, 999)) + random.choice(alphabet)
                random_int = random.randint(1,3)
                if random_int == 1:
                  propertyname = leet(propertyname)
                elif random_int == 2:
                  propertyname = leet(propertyname[:10] + fake.name())

              elif random_int == 8:
                propertyname = random.choice(alphabet) + str(random.randint(1, 999)) + fake.company() + fake.street_name()
                random_int = random.randint(1,3)
                if random_int == 1:
                  propertyname = leet(propertyname)
                elif random_int == 2:
                  propertyname = leet(propertyname[:10] + fake.name())

              elif random_int == 9:
                propertyname = fake.street_name() + fake.street_name() + str(random.randint(1, 999)) + random.choice(alphabet)
                random_int = random.randint(1,3)
                if random_int == 1:
                  propertyname = leet(propertyname)
                elif random_int == 2:
                  propertyname = leet(propertyname[:10] + fake.name())

              elif random_int == 10:
                propertyname = fake.company() + str(random.randint(1, 999)) + fake.street_name() + random.choice(alphabet)
                random_int = random.randint(1,3)
                if random_int == 1:
                  propertyname = leet(propertyname)
                elif random_int == 2:
                  propertyname = leet(propertyname[:10] + fake.name())

              elif random_int == 11:
                propertyname = random.choice(alphabet) + str(random.randint(1, 999)) + fake.street_name() + fake.company() + random.choice(["!", "NEW", "new", "(new)", "", 'Getaway!'])
                random_int = random.randint(1,3)
                if random_int == 1:
                  propertyname = leet(propertyname)
                elif random_int == 2:
                  propertyname = leet(propertyname[:10] + fake.name())

              elif random_int == 12:
                propertyname = fake.first_name() + str(random.randint(1, 999)) + random.choice(alphabet) + random.choice(["Best", "Renovated ", "(new)", "*NEW*"])
                random_int = random.randint(1,3)
                if random_int == 1:
                  propertyname = leet(propertyname)
                elif random_int == 2:
                  propertyname = leet(propertyname[:10] + fake.name())

              elif random_int == 13:
                propertyname = random.choice(["Best", "Renovated ", "(new)", "*NEW*"]) + fake.name() + str(random.randint(1, 999)) + random.choice(alphabet)
                random_int = random.randint(1,3)
                if random_int == 1:
                  propertyname = leet(propertyname)
                elif random_int == 2:
                  propertyname = leet(propertyname[:10] + fake.name())

              elif random_int == 14:
                propertyname = random.choice(alphabet) + str(random.randint(1, 999)) + fake.street_name() + fake.company() + fake.name()
                random_int = random.randint(1,3)
                if random_int == 1:
                  propertyname = leet(propertyname)
                elif random_int == 2:
                  propertyname = leet(propertyname[:10] + fake.name())

              else:
                propertyname = random.choice(["Stay With ", "The ", "(new)", "*NEW*"]) + fake.street_name() + random.choice(alphabet) + str(random.randint(1, 999)) + fake.company()
                random_int = random.randint(1,3)
                if random_int == 1:
                  propertyname = leet(propertyname)
                elif random_int == 2:
                  propertyname = leet(propertyname[:10] + fake.name())


            propertyname = propertyname.replace(' ', '-')
            street_number = random.randint(1, 999)
            street_name = fake.street_name().replace("'", "-")
            while len(street_name) > 20:
              street_name = fake.street_name().replace("'", "-")

            #apt_number can be null
            apt_numbers = [x for x in range(1, 999)]
            apt_numbers.append("NaN")
            apt_number = random.choice(apt_numbers)

            postal_code = ""
            for i in range(3):
              postal_code += random.choice(alphabet)
              postal_code += str(random.randint(1, 9))
            
            random_int = random.randint(1, 5)
            if random_int != 1:
              rent_rate = (round(random.randint(50, 300)/5)*5)
            else:
              rent_rate = (round(random.randint(50, 9999)/5)*5)
            
            property_type = random.choice(['entire', 'private', 'shared'])
            number_beds = random.randint(1, 10)
            number_baths = random.randint(1, 10)
            if number_beds < 2:
              max_guests = random.randint(1, 2)
            elif number_beds < 4:
              max_guests = random.randint(3, 5)
            elif number_beds < 6: 
              max_guests = random.randint(5, 8)
            elif number_beds <= 8: 
              max_guests = random.randint(8, 14)
            elif number_beds <= 10:
              max_guests = random.randint(10, 20)

            accessible = random.choice(['true', 'false'])
            pets_allowed = random.choice(['true', 'false'])

            random_int = random.randint(1, 13)
            if random_int == 1:
              r = requests.get('https://source.unsplash.com/random/?house')
            elif random_int == 2:
              r = requests.get('https://source.unsplash.com/random/?vacation')
            elif random_int == 3:
              r = requests.get('https://source.unsplash.com/random/?airbnb')
            elif random_int == 4:
              r = requests.get('https://source.unsplash.com/random/?hotel')
            elif random_int == 5:
              r = requests.get('https://source.unsplash.com/random/?apartment')
            elif random_int == 6:
              r = requests.get('https://source.unsplash.com/random/?dwelling')
            elif random_int == 7:
              r = requests.get('https://source.unsplash.com/random/?home')
            elif random_int == 8:
              r = requests.get('https://source.unsplash.com/random/?lodge')
            elif random_int == 9:
              r = requests.get('https://source.unsplash.com/random/?houseboat')
            elif random_int == 10:
              r = requests.get('https://source.unsplash.com/random/?inn')
            elif random_int == 11:
              r = requests.get('https://source.unsplash.com/random/?retreat')
            elif random_int == 12:
              r = requests.get('https://source.unsplash.com/random/?bed')
            elif random_int == 13:
              r = requests.get('https://source.unsplash.com/random/?room')

            random_name = secrets.token_hex(6)
            urllib.request.urlretrieve(r.url, "../static/images/" + random_name + ".png")
            picture = random_name + ".png"
            hostusername=username

            db.raw_query(f""" INSERT INTO property (propertyname, street_number, street_name, apt_number, province, postal_code, rent_rate, property_type, max_guests, number_beds, number_baths, accessible, pets_allowed, country, hostusername, picture) VALUES ('{propertyname}', '{street_number}', '{street_name}', '{apt_number}', '{province}', '{postal_code}', '{rent_rate}', '{property_type}', '{max_guests}', '{number_beds}', '{number_baths}', '{accessible}', '{pets_allowed}', '{country}', '{hostusername}', '{picture}')  """)

        ########payment method###########
        random_int = random.randint(1,2)
        if random_int == 1:
          card_type = random.choice(['mastercard', 'visa'])
          card_number = fake.credit_card_number()
          card_expiration = fake.date_between(start_date='+60d', end_date='+2y').strftime('%Y-%m-%d')
          cvv = random.randint(100, 999)
          db.raw_query(f""" INSERT INTO payment_method (username, card_type, first_name, last_name, card_number, card_expiration, cvv, billing_country) VALUES ('{username}', '{card_type}', '{first_name}', '{last_name}', '{card_number}', '{card_expiration}', '{cvv}', '{country}')  """)
        
        #######payout method#########
        random_int = random.randint(1,2)
        if random_int == 1:
          fake_paypal = fake.email()
          index_1 = fake_paypal.find("@") + 1
          paypal_address = fake_paypal[:index_1] + "paypal" + ".com"
          while len(paypal_address) > 20: 
            fake_paypal = fake.email()
            index_1 = fake_paypal.find("@") + 1
            paypal_address = fake_paypal[:index_1] + "paypal" + ".com"

          db.raw_query(f""" INSERT INTO payout_method (username, paypal_address) VALUES ('{username}', '{paypal_address}')  """)
          

  except Exception as e:
    db.close()
    db.new_connection()
    print(e)
    traceback.print_exc()


  db.commit()

#works_at
def works_at():
  try: 
    for i in range(len(countries)):
    #reduce_data = 5 
    #for i in range(reduce_data):
      completion = (i/(len(countries)))*100
      print("assigning employees to properties.... " + str(round(completion, 2)) + "% done")
      country = countries[i].replace("'", "-")
      if len(country) > 20:
          continue
      db.raw_query(f""" select username, title from employees where country='{country}' """)
      workers = db.fetch_all()
      #country has no workers (too little data generated)
      if workers != None:
        for worker in workers:
          username = worker[0]
          title = worker[1]
          if (title != "Branch Manager") and (title != "Admin"):
            db.raw_query(f""" select propertyname from property where country='{country}' order by random() limit 1 """)
            work_property = db.fetch_one()
            if work_property == None:
              continue
            propertyname = work_property[0]
            db.raw_query(f""" INSERT INTO works_at (employeeusername, propertyname) VALUES ('{username}', '{propertyname}') """)

  except Exception as e:
    db.close()
    db.new_connection()
    print(e)
    traceback.print_exc()

  db.commit()

#rental_agreement, property_taken_dates, payment too?
def insert_rental_agreement():
  try: 
    db.raw_query(f""" select username, work from users """)
    users = db.fetch_all()
    progress = 0
    for user in users:
      progress += 1
      completion = (progress/(len(users)))*100
      print("generating rental agreements.... " + str(round(completion, 2)) + "% done")
      username = user[0]
      work = user[1]
      random_int = random.randint(1, 3)
      if (work != "AirBnB Employee") and (random_int != 1):
        random_int = random.randint(1, 2)
        for i in range(random_int):
          db.raw_query(f""" select propertyname, hostusername, rent_rate from property order by random() limit 1 """)
          rent_property = db.fetch_one()
          propertyname = rent_property[0]
          hostusername = rent_property[1]
          if hostusername == username:
            continue
          rent_rate = rent_property[2] 
          random_start_delta = random.randint(1, 90)
          random_interval_delta = random.randint(1, 3)
          positive_or_negative = random.choice(['+', '-'])
          start_date = fake.date_between(start_date=positive_or_negative + str(random_start_delta) + 'd', end_date='+92d')
          end_date = start_date + datetime.timedelta(days=random_interval_delta)

          dates = []
          for number_days in range(random_interval_delta):
            date = start_date + datetime.timedelta(days=number_days)
            dates.append(date)
          #if one of the dates is taken, this stay isnt valid
          is_valid = True
          for date in dates:
            taken_date = date.strftime('%Y-%m-%d')
            #see if its a valid date
            db.raw_query(f""" select * from property_taken_dates where propertyname='{propertyname}' and taken_date='{taken_date}'  """)
            already_exists = db.fetch_one()
            if already_exists != None:
              is_valid = False

          if is_valid == False:
            continue

          if start_date < datetime.date.today():
            sign_date = start_date - datetime.timedelta(days=random.randint(1, 10))
            host_accepted = 'true'
          else:
            host_accepted = random.choice(['true', 'false'])
            if host_accepted == 'true':
              sign_date = datetime.date.today() - datetime.timedelta(days=random.randint(1, 10))
            else:
              sign_date = 'null'
          
          travelling_for_work = random.choice(['true', 'false'])
          message_to_host = fake.text(100)
          total_price = random_interval_delta*rent_rate
          guestusername = username
          rental_id = secrets.token_hex(10)
          #if host signs off on agreement, need to reflect in property_taken_dates
          if sign_date != 'null':
            dates = []
            for number_days in range(random_interval_delta):
              date = start_date + datetime.timedelta(days=number_days)
              dates.append(date)
            for date in dates:
              taken_date = date.strftime('%Y-%m-%d')
              
              db.raw_query(f""" INSERT INTO property_taken_dates (propertyname, taken_date) VALUES ('{propertyname}', '{taken_date}') """)
            
            end_date_datetime = end_date
            start_date = start_date.strftime('%Y-%m-%d')
            end_date = end_date.strftime('%Y-%m-%d')

            db.raw_query(f""" INSERT INTO rental_agreement (rental_id, start_date, end_date, sign_date, travelling_for_work, message_to_host, total_price, host_accepted, propertyname, guestusername, hostusername) VALUES ('{rental_id}', '{start_date}', '{end_date}', '{sign_date}', '{travelling_for_work}', '{message_to_host}', '{total_price}', '{host_accepted}', '{propertyname}', '{guestusername}', '{hostusername}') """)

            #create a deposit and a final payment
            if end_date_datetime <= datetime.date.today():
              for payment in range(2):
                payment_id = secrets.token_hex(10)
                if payment == 0:
                  is_deposit = 'true'
                  amount = float(total_price)*0.20
                  status = 'approved'
                else:
                  is_deposit = 'false'
                  amount = float(total_price)*0.80
                  status = random.choice(['approved', 'pending', 'approved'])
                
                db.raw_query(f""" INSERT INTO payment (payment_id, is_deposit, amount, status, rental_id, guestusername, hostusername) VALUES ('{payment_id}', '{is_deposit}', '{amount}', '{status}', '{rental_id}', '{guestusername}', '{hostusername}') """)

            #create only deposit
            else:
              payment_id = secrets.token_hex(10)
              is_deposit = 'true'
              amount = float(total_price)*0.20
              status = random.choice(['pending', 'approved'])
              db.raw_query(f""" INSERT INTO payment (payment_id, is_deposit, amount, status, rental_id, guestusername, hostusername) VALUES ('{payment_id}', '{is_deposit}', '{amount}', '{status}', '{rental_id}', '{guestusername}', '{hostusername}') """)

          else: 
            start_date = start_date.strftime('%Y-%m-%d')
            end_date = end_date.strftime('%Y-%m-%d')
            db.raw_query(f""" INSERT INTO rental_agreement (rental_id, start_date, end_date, sign_date, travelling_for_work, message_to_host, total_price, host_accepted, propertyname, guestusername, hostusername) VALUES ('{rental_id}', '{start_date}', '{end_date}', {sign_date}, '{travelling_for_work}', '{message_to_host}', '{total_price}', '{host_accepted}', '{propertyname}', '{guestusername}', '{hostusername}') """)
            #no payment row created here, because host must sign rental agreement before user deposits


  except Exception as e:
    db.close()
    db.new_connection()
    print(e)
    traceback.print_exc()

  db.commit()

#conversation and conversation_messages
def insert_conversations():
  try: 
    db.raw_query(f""" select username, join_date from users """)
    users = db.fetch_all()
    progress = 0
    for user in users:
      progress += 1
      completion = (progress/(len(users)))*100
      print("generating conversations.... " + str(round(completion, 2)) + "% done")
      senderusername = user[0]
      join_date = user[1]
      random_int = random.randint(0, 2) #cam increase this with large amount of data
      for i in range(random_int):
        db.raw_query(f""" select username from users order by random() limit 1 """)
        receiverusername = db.fetch_one()[0]
        if receiverusername == senderusername:
          continue 
        db.raw_query(f""" select * from conversation where senderusername='{senderusername}' and receiverusername='{receiverusername}' """)
        already_exists = db.fetch_one()
        #if the convo already exists, skip it to prevent primary key clash
        if already_exists != None:
          continue
        db.raw_query(f""" INSERT INTO conversation (senderusername, receiverusername) VALUES ('{senderusername}', '{receiverusername}') """)
        time = fake.date_time_between_dates(datetime_start=join_date, datetime_end=datetime.datetime.utcnow(), tzinfo=None)
        message_content = fake.text(100)
        db.raw_query(f""" INSERT INTO conversation_messages (senderusername, receiverusername, time, message_content) VALUES ('{senderusername}', '{receiverusername}', '{time}', '{message_content}') """)

  except Exception as e:
    db.close()
    db.new_connection()
    print(e)
    traceback.print_exc()

  db.commit()

#property_review and property_review_details, user_review, user_review_details
def insert_reviews():
  try: 
    todays_date = datetime.date.today().strftime('%Y-%m-%d')
    #people who write reviews have completed their valid rental_agreements
    db.raw_query(f""" select guestusername, propertyname, hostusername from rental_agreement where end_date<='{todays_date}' and host_accepted='true' """)
    stays = db.fetch_all()
    progress = 0
    for stay in stays:
      progress += 1
      completion = (progress/(len(stays)))*100
      print("generating reviews.... " + str(round(completion, 2)) + "% done")
      username = stay[0]
      propertyname = stay[1]
      hostusername = stay[2]
      db.raw_query(f""" select join_date from users where username='{username}' """)
      join_date = db.fetch_one()[0]
      ######## PROPERTY REVIEWS ###########
      #not all people write reviews
      random_int = random.randint(1,2)
      if random_int == 1:
        db.raw_query(f""" INSERT INTO property_review (username, propertyname) VALUES ('{username}', '{propertyname}') """)
        time = fake.date_time_between_dates(datetime_start=join_date, datetime_end=datetime.datetime.utcnow(), tzinfo=None)
        #communication
        integer = random.randint(1,5)
        if integer == 5:
          communication = integer
        else:
          decimal = round((random.randint(1,9))/10, 1)
          communication = integer + decimal
        
        #value
        integer = random.randint(1,5)
        if integer == 5:
          value = integer
        else:
          decimal = round((random.randint(1,9))/10, 1)
          value = integer + decimal
        
        #check_in
        integer = random.randint(1,5)
        if integer == 5:
          check_in = integer
        else:
          decimal = round((random.randint(1,9))/10, 1)
          check_in = integer + decimal
        
        #accuracy
        integer = random.randint(1,5)
        if integer == 5:
          accuracy = integer
        else:
          decimal = round((random.randint(1,9))/10, 1)
          accuracy = integer + decimal
        
        #cleanliness
        integer = random.randint(1,5)
        if integer == 5:
          cleanliness = integer
        else:
          decimal = round((random.randint(1,9))/10, 1)
          cleanliness = integer + decimal
        
        #location
        integer = random.randint(1,5)
        if integer == 5:
          location = integer
        else:
          decimal = round((random.randint(1,9))/10, 1)
          location = integer + decimal
        
        review_content = fake.text(150)

        db.raw_query(f""" INSERT INTO property_review_details (username, propertyname, time, communication, value, check_in, accuracy, cleanliness, location, review_content) VALUES ('{username}', '{propertyname}', '{time}', '{communication}', '{value}', '{check_in}', '{accuracy}', '{cleanliness}', '{location}', '{review_content}') """)
      ######## USER REVIEWS ###########
      #not all people write reviews
      random_int = random.randint(1,2)
      if random_int == 1:
        reviewerusername = username
        revieweeusername = hostusername
        db.raw_query(f""" INSERT INTO user_review (reviewerusername, revieweeusername) VALUES ('{reviewerusername}', '{revieweeusername}') """)

        time = fake.date_time_between_dates(datetime_start=join_date, datetime_end=datetime.datetime.utcnow(), tzinfo=None)
        review_content = fake.text(150)
        db.raw_query(f""" INSERT INTO user_review_details (reviewerusername, revieweeusername, time, review_content) VALUES ('{reviewerusername}', '{revieweeusername}', '{time}', '{review_content}') """)

  except Exception as e:
    db.close()
    db.new_connection()
    print(e)
    traceback.print_exc()

  db.commit()

def reset():
  db.raw_query("""

  drop table admins, branches, conversation, users, conversation_messages, employees, payment, payment_method,
  payout_method, person, person_email_address, person_phone_number, property, property_taken_dates, property_review, 
  property_review_details, rental_agreement, user_review, user_review_details, works_at CASCADE

  """)
  db.commit()
  
  files = glob.glob('../static/images/*')
  for f in files:
    if f == "../static/images/default.png":
      continue
    else:
      os.remove(f)

def create_admin():
  try:
    username = 'admin'
    password = 'admin'
    first_name = fake.first_name()
    middle_name = ' '
    last_name = fake.last_name()
    street_number = random.randint(1, 99)
    street_name = fake.street_name()
    apt_number = random.randint(1, 999)
    postal_code = ""
    for i in range(3):
      postal_code += random.choice(alphabet)
      postal_code += str(random.randint(1, 9))
    date_of_birth = fake.date()
    country = 'Canada'
    province = 'Ontario'
    salary = '100000'
    title = 'Master Admin'
    managerusername = 'admin'

    email = fake.email()
    while len(email) > 20:
      email = fake.email()

    phone_number = fake.phone_number().replace('.', '-').split('x')[0]
    while len(phone_number) > 20:
      phone_number = fake.phone_number().replace('.', '-').split('x')[0]

    work = "AirBnB Employee"

    join_date = fake.date_between(start_date='-60d', end_date='today').strftime('%Y-%m-%d')

    db.raw_query(f"""INSERT INTO person (username, first_name, middle_name, last_name, password, street_number, street_name, apt_number,
                postal_code, date_of_birth, country, province) VALUES ('{username}', '{first_name}', '{middle_name}', '{last_name}', 
                '{password}', '{street_number}', '{street_name}', '{apt_number}', '{postal_code}', '{date_of_birth}', '{country}', '{province}')""")
    
    db.raw_query(f"""INSERT INTO employees (username, title, salary, country, managerusername) VALUES ('{username}', '{title}', '{salary}', '{country}', '{managerusername}')""")
    
    db.raw_query(f"""INSERT INTO admins (username) VALUES ('{username}')""")

    db.raw_query(f"""INSERT INTO users (username, join_date, verified, about, languages, work, profile_picture) VALUES ('{username}', '{join_date}', 'false', 'N/A', 'English', '{work}', 'default.png')""")
    db.raw_query(f"insert into person_phone_number (username, phone_number) VALUES ('{username}', '{phone_number}')")
    db.raw_query(f"insert into person_email_address (username, email_address) VALUES ('{username}', '{email}')")

  except Exception as e:
    db.close()
    db.new_connection()
    print(e)
    traceback.print_exc()

  db.commit()

def main(): 
  try:
    generation_size = sys.argv[1].lower()
    if generation_size not in ['small', 'medium', 'large']:
      if generation_size == 'reset':
        reset()
        print("Reset successful, ready for data to be generated.")
        db.close()
        db.new_connection()
      else:
        print("Command not recognized, proceeding with generating a medium (recommended) dataset...")
        generation_size = 'medium'
  except IndexError as e:
    print("Generating a medium (recommended) dataset...")
    generation_size = 'medium'
  if generation_size != 'reset':
    try: 
      print("Creating tables...")
      create_all_tables()
      print("Creating branches...")
      insert_branches()
      create_alot(generation_size)
      print("Assigning employees properties to work at...")
      works_at()
      print("Creating rental_agreements...")
      insert_rental_agreement()
      print("Generating conversations...")
      insert_conversations()
      print("Generating reviews...")
      insert_reviews()
      print("Creating a master admin account...")
      create_admin()
      print("Successful data generation! \nTo log in, use the credentials: \n  username: admin \n  password: admin")

    except Exception as e:
      print(e)
      db.close()
      db.new_connection()

if __name__ == "__main__":
  main()
