from celery import shared_task

from marvel.models import Character
from myblog.settings.base import Marvel_PRIVATE_KEY, Marvel_PUBLIC_KEY
from services.marvel.exceptions import MarvelException, BadInputException
from services.marvel.marvel import Marvel
from django.core.cache import caches

redis_cache = caches['default']
redis_client = redis_cache.client.get_client()


@shared_task(name='base_marvel_info')
def base_marvel_info():
    marvel = Marvel(Marvel_PRIVATE_KEY, Marvel_PUBLIC_KEY)
    try:
        result = marvel.characters.all()
        redis_client.set('attributionHTML', result.get('attributionHTML', None))
        redis_client.set('attributionText', result.get('attributionText', None))
        redis_client.set('all_hero', result['data'].get('total'))
    except (MarvelException, BadInputException) as e:
        return e
    return 'success'


@shared_task(name="hero")
def hero_data():
    all_hero = redis_client.get('all_hero')
    marvel = Marvel(Marvel_PRIVATE_KEY, Marvel_PUBLIC_KEY)
    # for hero_id in all_hero:
    origin_data = marvel.characters.get('1011334')
    data = origin_data['data']['results'][0]
    update_dict = {
        "name": data['name'],
        "description": data['description'],
        "modified": data['modified'],
        "thumbnail": data['thumbnail']['path'],
        "resource_uri": data['resourceURI']
    }
    hero, created = Character.objects.get_or_create(unique_id=data['id'])
    return
