import asyncio
from TikTokApi import TikTokApi

async def main():
    # Initialize the TikTokApi instance
    async with TikTokApi() as api:
        # Create a session to interact with the API
        await api.create_sessions(ms_tokens=["dummy_token"], num_sessions=1, sleep_after=3)
        
        # Example: Fetch trending videos
        print("Fetching trending videos...")
        async for video in api.trending.videos(count=5):
            print(f"Video ID: {video.id} | Author: {video.author.username}")

if __name__ == "__main__":
    asyncio.run(main())
