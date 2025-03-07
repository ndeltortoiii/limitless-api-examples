from openai import OpenAI


def summarize_lifelogs(lifelogs, should_stream=True):
  client = OpenAI()
    
  response = client.chat.completions.create(
      model="gpt-4o-mini",
      messages=[
          {"role": "system", "content": "You are a helpful assistant that summarizes transcripts."},
          {"role": "user", "content": f"Summarize the following transcripts: {lifelogs}"}
      ],
      stream=should_stream
  )
  if should_stream:
    for chunk in response:
      if chunk.choices[0].finish_reason is None:
        print(chunk.choices[0].delta.content, end='')
  else:
    return response.choices[0].message.content
