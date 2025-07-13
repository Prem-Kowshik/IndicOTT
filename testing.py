from supabase import Client, create_client
import json
def return_genres():
    url="https://nglhfmgdfjqfqlzzgxnx.supabase.co"
    key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5nbGhmbWdkZmpxZnFsenpneG54Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTA0MDY5NTUsImV4cCI6MjA2NTk4Mjk1NX0.48CedgwhBkOGIOY-SydVKe8QIXZhm7phXnDQQP90TD4"
    supabase: Client= create_client(url,key)
    response=(supabase.table("Genre Data").select('*').execute())
    genres={}
    for i in response.data:
        if i['genre'] not in genres.keys():
            genres[i['genre']]=[]
        genres[i['genre']].append({"title":i['title'], "url":i['url']})
    return genres
def return_genres_indiancine():
    url="https://hzzsvriqrsxuovlrtzco.supabase.co"
    key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imh6enN2cmlxcnN4dW92bHJ0emNvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTIwNDY2MjAsImV4cCI6MjA2NzYyMjYyMH0.G__GVeZZIXSV-w-_c4XYILG8HIG1OtRGV-63L00Vziw"
    supabase: Client= create_client(url,key)
    response=(supabase.table("Video_movies").select('*').execute())
    genres={}
    for i in response.data:
        if i['genre'] not in genres.keys():
            genres[i['genre']]=[]
        genres[i['genre']].append({"title":i['title'], "url":i['url']})
    return genres
def return_language_classification():
    url="https://hzzsvriqrsxuovlrtzco.supabase.co"
    key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imh6enN2cmlxcnN4dW92bHJ0emNvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTIwNDY2MjAsImV4cCI6MjA2NzYyMjYyMH0.G__GVeZZIXSV-w-_c4XYILG8HIG1OtRGV-63L00Vziw"
    supabase: Client= create_client(url,key)
    response=(supabase.table("Video_movies").select('*').execute())
    languages={}
    for i in response.data:
        if i['language'] not in languages.keys():
            languages[i['language']]=[]
        languages[i['language']].append({"title":i['title'], "url":i['url']})
    return languages
def return_director_classification():
    url="https://hzzsvriqrsxuovlrtzco.supabase.co"
    key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imh6enN2cmlxcnN4dW92bHJ0emNvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTIwNDY2MjAsImV4cCI6MjA2NzYyMjYyMH0.G__GVeZZIXSV-w-_c4XYILG8HIG1OtRGV-63L00Vziw"
    supabase: Client= create_client(url,key)
    response=(supabase.table("Video_movies").select('*').execute())
    directors={}
    for i in response.data:
        if i['director'] not in directors.keys():
            directors[i['director']]=[]
        directors[i['director']].append({"title":i['title'], "url":i['url']})
    return directors
def return_year_wise_classification():
    url="https://hzzsvriqrsxuovlrtzco.supabase.co"
    key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imh6enN2cmlxcnN4dW92bHJ0emNvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTIwNDY2MjAsImV4cCI6MjA2NzYyMjYyMH0.G__GVeZZIXSV-w-_c4XYILG8HIG1OtRGV-63L00Vziw"
    supabase: Client= create_client(url,key)
    response=(supabase.table("Video_movies").select('*').execute())
    years={}
    for i in response.data:
        if i['year'] not in years.keys():
            years[i['year']]=[]
        years[i['year']].append({"title":i['title'], "url":i['url']})
    return years
