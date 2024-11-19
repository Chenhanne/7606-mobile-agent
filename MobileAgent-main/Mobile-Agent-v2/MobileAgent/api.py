import base64
import requests
import os
import openai
import httpx
from httpcore import RemoteProtocolError
from openai import OpenAI, RateLimitError, APITimeoutError
import time

SLEEP_TIME = 2
DELAY_TIME = 2



def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def inference_chat(chat, api_url, model, token):


    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    data = {
        "model": model,
        "messages": [],
        "max_tokens": 2048,
        'temperature': 0.0,
        "seed": 1234
    }

    for role, content in chat:
        data["messages"].append({"role": role, "content": content})

    try_times = 10
    while True:
        if try_times <= 0:
            break
        try:  # 原始是调用失败会无限调用，修改了一下
            res = requests.post(api_url, headers=headers, json=data)
            res_json = res.json()
            res_content = res_json['choices'][0]['message']['content']
        except:
            print("Network Error:")
            try_times -= 1
            try:
                print(res.json())
            except:
                print("Request Failed")
        else:
            break
    
    return res_content


'''
    delay = DELAY_TIME
    message = []
    retries = 5
    res_content = ""

    for role, content in chat:
        message.append({"role": role, "content": content})

    # 定义一个函数来处理分段
    def process_in_chunks(messages, chunk_size):
        for i in range(0, len(messages), chunk_size):
            yield messages[i:i + chunk_size]

    chunk_size = 15000  # 每次处理15000个tokens

    for chunk in process_in_chunks(message, chunk_size):
        while True:
            if retries <= 0:
                break

            try:
                response = completion = client.chat.completions.create(
                    model=model,
                    messages=chunk,
                    stream=True,
                    temperature=0.1,
                    top_p=0.1,
                )
                res_content = response.choices[0].message.content

                break  # 成功处理后跳出循环
            except RateLimitError as e:
                print(f"Rate limit exceeded. Sleeping for {SLEEP_TIME} seconds. Error: {e}")
                time.sleep(SLEEP_TIME)
            except APITimeoutError as e:
                retries -= 1
                if retries > 0:
                    print(f"Request timed out. Retrying in {delay} seconds... ({retries} retries left)")
                    time.sleep(delay)
                    delay *= 2  # Exponential backoff
                else:
                    print(f"Request timed out after multiple attempts. Error: {e}")
                    raise
            except httpx.HTTPStatusError as e:
                retries -= 1
                if retries > 0:
                    print(f"Request timed out. Retrying in {delay} seconds... ({retries} retries left)")
                    time.sleep(delay)
                    delay *= 2  # Exponential backoff
                else:
                    print(f"HTTP error occurred: {e}")
                    raise
            except RemoteProtocolError as e:
                retries -= 1
                if retries > 0:
                    print(f"Request timed out. Retrying in {delay} seconds... ({retries} retries left)")
                    time.sleep(delay)
                    delay *= 2  # Exponential backoff
                else:
                    print(f"Remote protocol error occurred: {e}")
                    raise
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                raise

    return res_content

'''
