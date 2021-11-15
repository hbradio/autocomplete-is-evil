import json
import tensorflow as tf


def lambda_handler(event, context):
    queryParams = event.get("queryStringParameters", {})
    phrase = queryParams.get("phrase", "Hello, ")
    type = queryParams.get("type", "shakespeare001")

    completion = getCompletion(type, phrase)

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
        },
        "body": json.dumps({
            "type": type,
            "phrase": phrase,
            "completion": completion
        }),
    }

def getCompletion(type, phrase):
    if type == "shakespeare001":
        model_file = 'one_step_shakespeare_100'
    elif type == "hitler001":
        model_file = 'one_step_hitler_100'
    elif type == "kjv001":
        model_file = 'one_step_kjv_100'
    elif type == "trump001":
        model_file = 'one_step_trump_100'
    elif type == "trumptweets001":
        model_file = 'one_step_trump_tweets_15'
    elif type == "dccc001":
        model_file = 'one_step_dccc_24'
    elif type == "gopaz001":
        model_file = 'one_step_gop_az_33'
    else:
        model_file = 'one_step_shakespeare_100'

    model = tf.keras.models.load_model('/opt/ml/models/' + model_file, compile=False)

    states = None
    next_char = tf.constant([phrase])
    result = [next_char]

    for n in range(100):
        next_char, states = model.generate_one_step(next_char, states=states)
        if next_char != '\n':
            result.append(next_char)
        if n > 10 and next_char in ('.', ',', ';', '!', '?', '\n'):
            break

    return tf.strings.join(result)[0].numpy().decode("utf-8")[len(phrase):]
