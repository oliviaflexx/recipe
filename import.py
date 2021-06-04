from recipe_scrapers import scrape_me
import sys

scraper = scrape_me('https://www.budgetbytes.com/beef-and-cauliflower-taco-skillet/')

sys.stdout = open("errors.txt", "w")

print(f'title {scraper.title()}')
print(f'time {scraper.total_time()}')
print(f'yield {scraper.yields()}')
print(f'ingredients {scraper.ingredients()}')
print(f'instructions {scraper.instructions()}')
print(f'image {scraper.image()}')
print(f'host {scraper.host()}')
print(f'links {scraper.links()}')
print(f'nutrients {scraper.nutrients()}')

sys.stdout.close()