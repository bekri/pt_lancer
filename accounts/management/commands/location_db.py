from django.core.management.base import BaseCommand
from accounts.models import Country, City

class Command(BaseCommand):
    help = 'Populate the database with countries and cities'

    def handle(self, *args, **kwargs):
        # List of countries and cities
        data = {
            'Tunisia': [
                'Tunis', 'Sfax', 'Sousse', 'Bizerte', 'Gabes', 'Ariana', 'Gafsa', 'Monastir', 'Kairouan', 'Hammamet'
            ],
            'Egypt': [
                'Cairo', 'Alexandria', 'Giza', 'Sharm El Sheikh', 'Luxor', 'Aswan', 'Hurghada', 'Port Said', 'Mansoura', 'Ismailia'
            ],
            'Saudi Arabia': [
                'Riyadh', 'Jeddah', 'Mecca', 'Medina', 'Dammam', 'Khobar', 'Dhahran', 'Jubail', 'Taif', 'Abha'
            ],
            'Qatar': [
                'Doha', 'Al Wakrah', 'Al Khor', 'Al Rayyan', 'Umm Salal', 'Mesaieed', 'Al Daayen', 'Madinat ash Shamal'
            ],
            'United Arab Emirates (UAE)': [
                'Dubai', 'Abu Dhabi', 'Sharjah', 'Ajman', 'Fujairah', 'Ras Al Khaimah', 'Umm Al Quwain'
            ],
            'Kuwait': [
                'Kuwait City', 'Al Ahmadi', 'Hawalli', 'Farwaniya', 'Jahra'
            ],
            'Oman': [
                'Muscat', 'Salalah', 'Sohar', 'Nizwa', 'Sur'
            ],
            'Bahrain': [
                'Manama', 'Muharraq', 'Riffa', 'Hamad Town', 'Isa Town'
            ],
            'Jordan': [
                'Amman', 'Zarqa', 'Irbid', 'Madaba', 'Aqaba'
            ],
            'Lebanon': [
                'Beirut', 'Tripoli', 'Sidon', 'Tyre', 'Jounieh'
            ],
            'Syria': [
                'Damascus', 'Aleppo', 'Homs', 'Latakia', 'Hama'
            ],
            'Turkey': [
                'Istanbul', 'Ankara', 'Izmir', 'Bursa', 'Antalya'
            ],
            'Cyprus': [
                'Nicosia', 'Limassol', 'Larnaca', 'Paphos', 'Famagusta'
            ],
            'France': [
                'Paris', 'Marseille', 'Lyon', 'Toulouse', 'Nice'
            ],
            'Germany': [
                'Berlin', 'Munich', 'Hamburg', 'Frankfurt', 'Cologne'
            ],
            'Italy': [
                'Rome', 'Milan', 'Naples', 'Turin', 'Florence'
            ],
            'Spain': [
                'Madrid', 'Barcelona', 'Valencia', 'Seville', 'Bilbao'
            ],
            'United Kingdom': [
                'London', 'Manchester', 'Birmingham', 'Edinburgh', 'Glasgow'
            ],
            'Netherlands': [
                'Amsterdam', 'Rotterdam', 'The Hague', 'Utrecht', 'Eindhoven'
            ],
            'Belgium': [
                'Brussels', 'Antwerp', 'Ghent', 'Bruges', 'Liege'
            ],
            'Morocco': [
                'Casablanca', 'Marrakech', 'Rabat', 'Tangier', 'Fes', 'Kenitra', 'Salé'
            ],
            'United States': [
                'New York City', 'Los Angeles', 'Chicago', 'Houston', 'San Francisco'
            ],
            'Russia': [
                'Moscow', 'Saint Petersburg', 'Novosibirsk', 'Yekaterinburg', 'Kazan'
            ],
            'Canada': [
                'Toronto', 'Vancouver', 'Montreal', 'Calgary', 'Edmonton', 'Ottawa', 'Quebec City', 'Winnipeg', 'Halifax', 'Hamilton'
            ],
            'Portugal': [
                'Lisbon', 'Porto', 'Vila Nova de Gaia', 'Braga', 'Amadora'
            ],
        }

        for country_name, cities in data.items():
            country, created = Country.objects.get_or_create(name=country_name)
            for city_name in cities:
                City.objects.get_or_create(name=city_name, country=country)

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with countries and cities'))
