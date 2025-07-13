from supabase import Client, create_client
import asyncio
def return_video_data():
    url="https://hzzsvriqrsxuovlrtzco.supabase.co"
    key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imh6enN2cmlxcnN4dW92bHJ0emNvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTIwNDY2MjAsImV4cCI6MjA2NzYyMjYyMH0.G__GVeZZIXSV-w-_c4XYILG8HIG1OtRGV-63L00Vziw"
    supabase: Client=create_client(url,key)
    response=(supabase.table("Movies_with_embedded_video").select("*").execute())
    return response.data    

