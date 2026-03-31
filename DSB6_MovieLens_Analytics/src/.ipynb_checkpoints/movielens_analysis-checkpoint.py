#!/usr/bin/env python3
from datetime import datetime
import pytest
import csv
from collections import OrderedDict, Counter
import requests
from bs4 import BeautifulSoup
import re

class Ratings:
    """
    Анализ данных из файла ratings.csv
    """
    def __init__(self, path_to_the_file):
        
        self.userIds = []
        self.movieIds = []
        self.ratings_list = []
        self.timestamps = []
        self.years = []
        self.ratings_data = []

        try:
            with open(path_to_the_file, 'r', encoding='utf-8') as file:
                next(file)

                for i, line in enumerate(file):
                    if i >= 1000:
                        break

                    line = line.strip()
                    if not line:
                        continue

                    parts = line.split(',')
                    if len(parts) >= 4:
                        user_id = int(parts[0])
                        movie_id = int(parts[1])
                        rating = float(parts[2])
                        timestamp = int(parts[3])
                        year = datetime.fromtimestamp(timestamp).year
                        
                        self.userIds.append(user_id)
                        self.movieIds.append(movie_id)
                        self.ratings_list.append(rating)
                        self.timestamps.append(timestamp)
                        self.years.append(year)
                        
                        self.ratings_data.append({
                            'userId': user_id,
                            'movieId': movie_id,
                            'rating': rating,
                            'timestamp': timestamp,
                            'year': year
                        })
                
        except FileNotFoundError:
            print(f"Error: File {path_to_the_file} not found")
            raise
        except Exception as e:
            print(f"Error reading file: {e}")
            raise

    @staticmethod
    def median(data):
        """Вычисление медианы"""
        if not data:
            return 0
        sorted_data = sorted(data)
        n = len(sorted_data)
        mid = n // 2
        if n % 2 == 1:
            return sorted_data[mid]
        return (sorted_data[mid - 1] + sorted_data[mid]) / 2  

    @staticmethod
    def variance(data):
        """Вычисление дисперсии (средний квадрат отклонения от среднего значения)"""
        n = len(data)
        if n < 2:
            return 0
        mean = sum(data) / n
        return sum((x - mean) ** 2 for x in data) / (n - 1) 
    
    class Movies:
        """
        Внутренний класс для анализа рейтингов фильмов
        """
        def __init__(self, ratings_data, movies_data):
            self.ratings = ratings_data
            self.movie_titles = movies_data
        
        def dist_by_year(self):
            """
            Подсчитывает количество оценок фильмов по годам 
            и сортирует по возврастанию по годам.
            """
            years = {}
            for rating in self.ratings:
                year = rating['year']
                years[year] = years.get(year, 0) + 1
            
            return OrderedDict(sorted(years.items()))
        
        def dist_by_rating(self):
            """
            Подсчитывает сколько раз встречалась каждая оценка 
            и сортирует по возрастанию по количеству оценок.
            """
            ratings_dist = {}
            for rating in self.ratings:
                ratings_dist[rating['rating']] = ratings_dist.get(rating['rating'], 0) + 1
            
            return OrderedDict(sorted(ratings_dist.items()))
        
        def top_by_num_of_ratings(self, n):
            """
            Находит фильмы, которые получили больше всего оценок 
            (самые популярные по количеству отзывов). 
            Результат — топ-N фильмов с наибольшим количеством оценок.
            """
            movie_counts = {}
            for rating in self.ratings:
                movie_counts[rating['movieId']] = movie_counts.get(rating['movieId'], 0) + 1
            
            result = []
            for movie_id, count in movie_counts.items():
                title = self.movie_titles.get(movie_id, f"Unknown {movie_id}")
                result.append((title, count))
            
            result.sort(key=lambda x: -x[1])
            return OrderedDict(result[:n])
        
        def top_by_ratings(self, n, metric='average'):
            """
            Фильмы с самыми высокими оценками 
            (по среднему или медианному значению).
            """
            movie_ratings = {}
            for rating in self.ratings:
                movie_id = rating['movieId']
                if movie_id not in movie_ratings:
                    movie_ratings[movie_id] = []
                movie_ratings[movie_id].append(rating['rating'])
            
            result = []
            for movie_id, ratings_list in movie_ratings.items():
                if metric == 'average':
                    value = sum(ratings_list) / len(ratings_list)
                elif metric == 'median':
                    value = Ratings.median(ratings_list)
                else:
                    value = 0
                
                title = self.movie_titles.get(movie_id, f"Unknown {movie_id}")
                result.append((title, round(value, 2)))
            
            result.sort(key=lambda x: -x[1])
            return OrderedDict(result[:n])
        
        def top_controversial(self, n):
            """
            Фильмы с наибольшим разбросом (дисперсией) оценок.
            """
            movie_ratings = {}
            for rating in self.ratings:
                movie_id = rating['movieId']
                if movie_id not in movie_ratings:
                    movie_ratings[movie_id] = []
                movie_ratings[movie_id].append(rating['rating'])
            
            result = []
            for movie_id, ratings_list in movie_ratings.items():
                if len(ratings_list) > 1:
                    variance = Ratings.variance(ratings_list)
                else:
                    variance = 0
                
                title = self.movie_titles.get(movie_id, f"Unknown {movie_id}")
                result.append((title, round(variance, 2)))
            
            # Сортировка по отклонению в нисходящем порядке
            result.sort(key=lambda x: -x[1])
            return OrderedDict(result[:n])
    
    class Users:
        """
        В этом классе три метода:
        1.Распределение пользователей по количеству выставленных ими оценок.
        2.Распределение пользователей по средним или медианным оценкам, выставленным ими.
        3.Топ-n пользователей с наибольшей разницей в рейтингах.
        """
        def __init__(self, ratings_data):
            self.ratings = ratings_data
        
        def dist_by_num_of_ratings(self):
            """
            Считает, сколько оценок поставил каждый пользователь, 
            и возвращает рейтинг пользователей по активности.
            """
            user_counts = {}
            for rating in self.ratings:
                user_counts[rating['userId']] = user_counts.get(rating['userId'], 0) + 1
            
            sorted_counts = sorted(user_counts.items(), key=lambda x: -x[1])
            return OrderedDict(sorted_counts)
        
        def dist_by_ratings(self, metric='average'):
            """
            Анализирует, какие оценки в среднем ставит каждый пользователь.
            """
            user_ratings = {}
            for rating in self.ratings:
                user_id = rating['userId']
                if user_id not in user_ratings:
                    user_ratings[user_id] = []
                user_ratings[user_id].append(rating['rating'])
            
            result = {}
            for user_id, ratings_list in user_ratings.items():
                if metric == 'average':
                    value = sum(ratings_list) / len(ratings_list)
                elif metric == 'median':
                    value = Ratings.median(ratings_list)
                else:
                    value = 0
                result[user_id] = round(value, 2)
            
            sorted_result = sorted(result.items(), key=lambda x: -x[1])
            return OrderedDict(sorted_result)
        
        def top_controversial(self, n):
            """
            Находит пользователей которые 
            ставят и очень высокие, и очень низкие оценки, 
            у кого максимальный "разброс" во мнениях.
            """
            user_ratings = {}
            for rating in self.ratings:
                user_id = rating['userId']
                if user_id not in user_ratings:
                    user_ratings[user_id] = []
                user_ratings[user_id].append(rating['rating'])
            
            result = []
            for user_id, ratings_list in user_ratings.items():
                if len(ratings_list) > 1:
                    variance = Ratings.variance(ratings_list)
                else:
                    variance = 0
                result.append((user_id, round(variance, 2)))
            
            result.sort(key=lambda x: -x[1])
            return OrderedDict(result[:n])


class Tags:
    """
    Анализ данных из файла tags.csv
    """
    def __init__(self, path_to_the_file):
        
        self.tags = []
        try:
            with open(path_to_the_file, 'r', encoding='utf-8') as f:
                next(f)
                for i, line in enumerate(f):
                    if i >= 1000:
                        break
                    parts = line.strip().split(',')
                    if len(parts) >= 3:
                        tag = parts[2].strip('"')
                        self.tags.append(tag.lower())
        except FileNotFoundError:
            print(f"Error: File {path_to_the_file} not found")
            raise
    
    def most_words(self, n):
        """
        Находит теги, состоящие из наибольшего количества слов.
        """
        # Убираем дубликаты и считаем слова в каждом (тег:количество слов)
        unique_tags = {}
        for tag in self.tags:
            if tag not in unique_tags:
                unique_tags[tag] = len(tag.split())
        
        sorted_tags = sorted(unique_tags.items(), key=lambda x: -x[1])
        return OrderedDict(sorted_tags[:n])
    
    def longest(self, n):
        """
        Находит самые длинные теги по количеству символов 
        (букв, пробелов, знаков препинания).
        """
        unique_tags = {}
        for tag in self.tags:
            if tag not in unique_tags:
                unique_tags[tag] = len(tag)
        
        sorted_tags = sorted(unique_tags.items(), key=lambda x: -x[1])
        return [tag for tag, _ in sorted_tags[:n]]
    
    def most_words_and_longest(self, n):
        """
        Находит теги, которые одновременно:
        1.Входят в топ-n по количеству слов (most_words)
        2.Входят в топ-n по количеству символов (longest)
        """
        most_words_tags = set(self.most_words(n).keys())
        longest_tags = set(self.longest(n))
        return list(most_words_tags & longest_tags)
    
    def most_popular(self, n):
        """
        Находит самые часто используемые теги, 
        которые пользователи добавляли к фильмам больше всего раз.
        """
        tag_counts = {}
        for tag in self.tags:
            tag_counts[tag] = tag_counts.get(tag, 0) + 1
        
        sorted_tags = sorted(tag_counts.items(), key=lambda x: -x[1])
        return OrderedDict(sorted_tags[:n])
    
    def tags_with(self, word):
        """
        Вводим слово, возвращает все теги, где это слово встречается.
        """
        word = word.lower()
        result = set()
        for tag in self.tags:
            if word in tag:
                result.add(tag)
        
        return sorted(list(result))

class Movies:
    """
    Анализ данных из файла movies.csv
    """
    def __init__(self, path_to_the_file):
        
        self.movies_data = []   # Список словарей
        self.movie_titles = {}  # Словарь {movieId: title}
        self.movie_genres = {}  # Словарь {movieId: [genres]}

        try:
            with open(path_to_the_file, 'r', encoding='utf-8') as file:
                next(file)
                for i, line in enumerate(file):
                    if i >= 1000:  
                        break

                    line = line.strip()
                    if not line:
                        continue

                    parts = line.split(',')
                    movie_id = int(parts[0])
                    title_parts = parts[1:-1] if len(parts) > 3 else [parts[1]]
                    title = ','.join(title_parts).strip('"')
                    genres_str = parts[-1]

                    self.movie_titles[movie_id] = title
                    
                    if genres_str == '(no genres listed)':
                        genres_list = []
                    else:
                        genres_list = genres_str.split('|')

                    self.movie_genres[movie_id] = genres_list
                    self.movies_data.append({
                        'movieId': movie_id,
                        'title': title,
                        'genres': genres_list
                    })

        except FileNotFoundError:
            print(f"Error: File {path_to_the_file} not found")
            raise
        except Exception as e:
            print(f"Error reading file: {e}")
            raise

    def dist_by_release(self):
        """
        Метод возвращает словарь где ключ - год выпуска фильма,
        значение - количество фильмов выпущенных в этом году.
        """
        years_count = Counter()
        year_pattern = re.compile(r'\((\d{4})\)$')

        for movie in self.movies_data:
            title = movie['title']
            match = year_pattern.search(title)
            if match:
                year = int(match.group(1))
                years_count[year] += 1
            else:
                years_count['Unknown'] += 1

        return OrderedDict(sorted(years_count.items(), key=lambda x: x[1], reverse=True))

    def dist_by_genres(self):
        """
        Метод возвращает словарь, где ключ - жанр, 
        значение - количество фильмов этого жанра.
        """
        genres_count = Counter()

        for movie in self.movies_data:
            for genre in movie['genres']:
                genres_count[genre] += 1

        return OrderedDict(sorted(genres_count.items(), key=lambda item: item[1], reverse=True))

    def most_genres(self, n):
        """
        Возвращать словарь с топ-n фильмами по количеству жанров, 
        где ключ - название фильма,
        значение - количество жанров фильма.
        """
        movies_with_genre_count = []

        for movie in self.movies_data:
            title = movie['title']
            num_genres = len(movie['genres'])
            movies_with_genre_count.append((title, num_genres))

        movies_with_genre_count.sort(key=lambda x: (-x[1], x[0]))

        return OrderedDict(movies_with_genre_count[:n])

class Links:
    def __init__(self, path_to_the_file):
        self.links = []
        try:
            with open(path_to_the_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for i, row in enumerate(reader):
                    if i >= 1000: break
                    self.links.append(row)
        except FileNotFoundError:
            raise FileNotFoundError(f"Файл {path_to_the_file} не найден")

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
    def _get_movie_info(self, imdb_id):
        url = f"https://www.imdb.com/title/tt{imdb_id}/"
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            if response.status_code != 200: return None
            soup = BeautifulSoup(response.text, 'html.parser')

            budget_tag = soup.find(text=re.compile(r'Budget'))
            budget = 0
            if budget_tag:
                b_val = budget_tag.find_next(text=re.compile(r'\d'))
                budget = int(re.sub(r'[^\d]', '', b_val)) if b_val else 0


            gross_tag = soup.find(text=re.compile(r'Gross worldwide'))
            gross = 0
            if gross_tag:
                g_val = gross_tag.find_next(text=re.compile(r'\d'))
                gross = int(re.sub(r'[^\d]', '', g_val)) if g_val else 0

            runtime = 0
            rt_tag = soup.find(text=re.compile(r'Runtime'))
            if rt_tag:
                rt_val = rt_tag.find_next(text=re.compile(r'\d'))
                if rt_val:
                    h = re.search(r'(\d+)h', rt_val.text)
                    m = re.search(r'(\d+)m', rt_val.text)
                    runtime = (int(h.group(1)) * 60 if h else 0) + (int(m.group(1)) if m else 0)

            director = "Unknown"
            dir_tag = soup.find(text=re.compile(r'Director'))
            if dir_tag:
                d_val = dir_tag.find_next('a')
                director = d_val.text if d_val else "Unknown"

            return {'director': director, 'budget': budget, 'gross': gross, 'runtime': runtime}
        except:
            return None

    def top_directors(self, n):
        directors = []
        for link in self.links:
            info = self._get_movie_info(link['imdbId'])
            if info: directors.append(info['director'])
        counts = Counter(directors)
        return OrderedDict(sorted(counts.items(), key=lambda x: x[1], reverse=True)[:n])

    def most_expensive(self, n):
        budgets = []
        for link in self.links:
            info = self._get_movie_info(link['imdbId'])
            if info: budgets.append((link['movieId'], info['budget']))
        return OrderedDict(sorted(budgets, key=lambda x: x[1], reverse=True)[:n])

    def most_profitable(self, n):
        profits = []
        for link in self.links:
            info = self._get_movie_info(link['imdbId'])
            if info:
                profit = info['gross'] - info['budget']
                profits.append((link['movieId'], profit))
        return OrderedDict(sorted(profits, key=lambda x: x[1], reverse=True)[:n])

    def top_cost_per_minute(self, n):
        costs = []
        for link in self.links:
            info = self._get_movie_info(link['imdbId'])
            if info and info['runtime'] > 0:
                cost = round(info['budget'] / info['runtime'], 2)
                costs.append((link['movieId'], cost))
        return OrderedDict(sorted(costs, key=lambda x: x[1], reverse=True)[:n])

class Tests:
    def test_median_calculation(self):
        from movielens_analysis import Ratings
        assert Ratings.median([1, 3, 5]) == 3
        assert Ratings.median([1, 2, 3, 4]) == 2.5
        assert Ratings.median([]) == 0

    def test_variance_calculation(self):
        from movielens_analysis import Ratings
        data = [1, 2, 3]
        assert Ratings.variance(data) == 1.0
        assert Ratings.variance([5]) == 0

    def test_ratings_init(self, ratings_obj):
        assert len(ratings_obj.ratings_data) <= 1000
        assert 'year' in ratings_obj.ratings_data[0]
        assert isinstance(ratings_obj.ratings_data[0]['rating'], float)

    def test_dist_by_year_types(self, ratings_movies_obj):
        res = ratings_movies_obj.dist_by_year()
        assert isinstance(res, OrderedDict)
        years = list(res.keys())
        assert years == sorted(years)

    def test_dist_by_rating_logic(self, ratings_movies_obj):
        res = ratings_movies_obj.dist_by_rating()
        assert isinstance(res, OrderedDict)
        for rating in res.keys():
            assert 0.5 <= rating <= 5.0

    def test_top_by_num_of_ratings(self, ratings_movies_obj):
        n = 5
        res = ratings_movies_obj.top_by_num_of_ratings(n)
        assert len(res) <= n
        counts = list(res.values())
        assert counts == sorted(counts, reverse=True)

    def test_top_by_ratings_average(self, ratings_movies_obj):
        n = 3
        res = ratings_movies_obj.top_by_ratings(n, metric='average')
        assert len(res) <= n
        for val in res.values():
            assert len(str(val).split('.')[-1]) <= 2

    def test_top_controversial_sorting(self, ratings_movies_obj):
        res = ratings_movies_obj.top_controversial(10)
        variances = list(res.values())
        assert variances == sorted(variances, reverse=True)

    def test_users_dist_by_num_of_ratings(self, ratings_users_obj):
        res = ratings_users_obj.dist_by_num_of_ratings()
        assert isinstance(res, OrderedDict)
        counts = list(res.values())
        assert counts == sorted(counts, reverse=True)
        assert isinstance(list(res.keys())[0], int)

    def test_users_dist_by_ratings_average(self, ratings_users_obj):
        res = ratings_users_obj.dist_by_ratings(metric='average')
        assert isinstance(res, OrderedDict)
        for val in res.values():
            assert 0.5 <= val <= 5.0

    def test_users_top_controversial(self, ratings_users_obj):
        n = 5
        res = ratings_users_obj.top_controversial(n)
        assert len(res) <= n
        variances = list(res.values())
        assert variances == sorted(variances, reverse=True)

    def test_tags_most_words(self, tags_obj):
        n = 5
        res = tags_obj.most_words(n)
        assert isinstance(res, OrderedDict)
        word_counts = list(res.values())
        assert word_counts == sorted(word_counts, reverse=True)

    def test_tags_longest_type(self, tags_obj):
        n = 3
        res = tags_obj.longest(n)
        assert isinstance(res, list)
        assert len(res) <= n
        if len(res) > 1:
            assert len(res[0]) >= len(res[1])

    def test_tags_most_words_and_longest(self, tags_obj):
        n = 10
        res = tags_obj.most_words_and_longest(n)
        assert isinstance(res, list)
        assert len(res) == len(set(res))

    def test_tags_most_popular(self, tags_obj):
        n = 5
        res = tags_obj.most_popular(n)
        assert isinstance(res, OrderedDict)
        counts = list(res.values())
        assert counts == sorted(counts, reverse=True)

    def test_tags_with_search(self, tags_obj):
        word = "sci-fi"
        res = tags_obj.tags_with(word)
        assert isinstance(res, list)
        for tag in res:
            assert word in tag.lower()
        assert res == sorted(res)

    def test_movies_dist_by_release_logic(self, movies_obj):
        res = movies_obj.dist_by_release()
        assert isinstance(res, OrderedDict)
        counts = list(res.values())
        assert counts == sorted(counts, reverse=True)
        for key in res.keys():
            assert isinstance(key, int) or key == 'Unknown'

    def test_movies_dist_by_genres_content(self, movies_obj):
        res = movies_obj.dist_by_genres()
        assert isinstance(res, OrderedDict)
        known_genres = {'Drama', 'Comedy', 'Action', 'Adventure'}
        assert any(genre in res for genre in known_genres)
        counts = list(res.values())
        assert counts == sorted(counts, reverse=True)

    def test_movies_most_genres_limit(self, movies_obj):
        n = 10
        res = movies_obj.most_genres(n)
        assert len(res) == n
        for count in res.values():
            assert isinstance(count, int)
        genre_counts = list(res.values())
        assert genre_counts == sorted(genre_counts, reverse=True)

    def test_movies_parsing_commas(self, movies_obj):
        for movie in movies_obj.movies_data:
            assert isinstance(movie['genres'], list)
            assert isinstance(movie['movieId'], int)

    def test_links_most_profitable_logic(self, links_obj):
        res = links_obj.most_profitable(3)
        assert isinstance(res, OrderedDict)
        values = list(res.values())
        assert values == sorted(values, reverse=True)

    def test_links_top_cost_rounding(self, links_obj):
        res = links_obj.top_cost_per_minute(1)
        if res:
            val = list(res.values())[0]
            assert round(val, 2) == val

@pytest.fixture
def ratings_obj():
    from movielens_analysis import Ratings
    return Ratings('../datasets/ratings.csv')

@pytest.fixture
def ratings_movies_obj(ratings_obj):
    mock_titles = {1: "Toy Story (1995)", 2: "Jumanji (1995)"}
    return ratings_obj.Movies(ratings_obj.ratings_data, mock_titles)

@pytest.fixture
def ratings_users_obj(ratings_obj):
    return ratings_obj.Users(ratings_obj.ratings_data)

@pytest.fixture
def tags_obj():
    from movielens_analysis import Tags
    return Tags('../datasets/tags.csv')

@pytest.fixture
def movies_obj():
    from movielens_analysis import Movies
    return Movies('../datasets/movies.csv')

@pytest.fixture
def links_obj():
    from movielens_analysis import Links
    links = Links('../datasets/links.csv')
    links.links = links.links[:5]
    return links

if __name__ == '__main__':
    print("Module movielens_analysis loaded successfully.")
