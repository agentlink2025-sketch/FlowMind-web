#pip install langchain-core
#pip install httpx[http2]
#curl ifconfig.me
#ipconfig172.17.0.7
import httpx
from openai import OpenAI
from langchain_core.prompts import MessagesPlaceholder,ChatPromptTemplate

def get_model(openai_api_base):
    """
    模型url
    """
    # Config().NER_WORD_MODEL_URL
    # setting.config[config.APP_ENV].NER_WORD_MODEL_URL
    httpx_client = httpx.Client(http2=True, verify=False)
    openai_api_key = "EMPTY"
    openai_api_base = openai_api_base

    model = OpenAI(
        api_key=openai_api_key,
        base_url=openai_api_base,
        http_client=httpx_client
    )
    print("model:")
    print(model)
    return model
def generate_ans(prompt):
    #INTENT_MODEL_URL = 'http://localhost:10052/v1'
    #INTENT_MODEL_URL = 'http://3q1-o5zmkylq4ipt75sby-kzhe2ezvq-custom.service.onethingrobot.com:10052/v1'
    #172.17.0.7
    #INTENT_MODEL_URL = 'http://172.17.0.3:10052/v1'
    #qjq-n7527ixuk1ttjbfq5-fzbecewvq-custom.service.onethingrobot.com	
    INTENT_MODEL_URL = "http://qjq-n7527ixuk1ttjbfq5-fzbecewvq-custom.service.onethingrobot.com/v1"
    try:
        qw_model = get_model(INTENT_MODEL_URL)
        print("qw_model:")
        print(qw_model)
    except Exception as e:
        print("qw_model error:")
        print(e)
        
    prompt = prompt.strip()
    wrong_list = ['视频解析失败', '视频下载失败', '视频为纯背景音', '视频未解析出语音']
    if prompt in wrong_list:
        return '{}'
    elif prompt == '' or len(prompt) <= 1:
        return '{}'
    else:
        prompts = '''这是一个全能小助手，请有效回答用户问题。

<文本>
"{text}"

'''

        # 接口vllm请求
        prompt_template = ChatPromptTemplate.from_template(prompts)
        new_prompt = prompt_template.invoke({'text':prompt}).to_string()[:7000]
        try:
            print("--new prompt--")
            print(new_prompt)
            chat_response = qw_model.chat.completions.create(
                            model='/root/LLaMA-Factory/qwen_model',
                            messages=[
                            {"role": "system", "content": 'you are a helpful assistant ' },
                            {"role": "user", "content": new_prompt}
                            ],
                            top_p=0.00000001,
                            max_tokens=200,
                            temperature=0.1

                        )
            print("--chat_response--")
            print(chat_response)
            response = chat_response.choices[0].message.content
        except Exception as e:
            print(e)
            response = '{}'
        return response
result = generate_ans("蛋炒饭怎么做？")
print("--result--")
print(result)