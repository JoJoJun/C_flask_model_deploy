from flask import Flask, make_response, Response, json, request
import sys
import os
import tensorflow as tf
import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()

model = Flask(__name__)

@model.route('/', methods=['POST', 'GET'])
def index():
    resp = make_response()
    resp.status_code = 200
    resp.headers['content-type'] = 'text/plain'
    resp.data = 'Please visit route \'/run_model/\''
    return resp

@model.route('/run_model/', methods=['POST'])
def model_run():
    ### 使用form_data形式发送POST请求
    ### USER_AUTHENTICATION
    user_key = request.form['key']
    if key != user_key:
        response = Response("Key Wrong!")
        return response
    #TODO: AUTHENTICATION
    ### DATA_PARSER
    data = request.form['data']
    data_str = str(data)
    try:
        input_data = json.loads(data_str)
    except:
        response = Response("Not Structed Input")
        return response
    ###

    input_1 = graph.get_tensor_by_name(input_node + ":0")
    feed_dict = {
        input_1: input_data
    }

    result = None
    try:
        run_result = sess.run(graph.get_tensor_by_name(output_node + ":0"), feed_dict)
        run_result = json.loads(str(run_result))
        result = {
            'status': 'success',
            'data': run_result
        }
    except:
        result = {
            'status': 'fail',
            'data': "Model Runtime Error"
        }
    response = Response(json.dumps(result),content_type='application/json',status=200)
    return response

def load_model(model_directory, model_graph, input_node_name, output_node_name):
    ## TODO: Log文件记录
    print("start load model")
    saver = tf.train.import_meta_graph(model_graph)
    saver.restore(sess, tf.train.latest_checkpoint(model_directory))  ##文件夹
    global graph
    graph = tf.get_default_graph()

    # 获取图结构中的所有节点
    nodes = [tensor.name for tensor in graph.as_graph_def().node]
    #print(nodes)

    ### default = input_node_name
    global input_node
    input_node = None
    try:
        input_node_test = graph.get_tensor_by_name(input_node_name + ":0")
        input_node = input_node_name
    except KeyError:
        try:
            ### else the input node
            input_node_test = graph.get_tensor_by_name("input:0")
            input_node = "input"
        except KeyError:
            ### else the first node
            input_node = nodes[0]

    ### default = output_node_name
    global output_node
    output_node = None
    try:
        output_node_test = graph.get_tensor_by_name(output_node_name + ":0")
        output_node = output_node_name
    except KeyError:
        try:
            ### else the output node
            output_node_test = graph.get_tensor_by_name("output:0")
            output_node = "output"
        except KeyError:
            ### else the last node
            output_node = nodes[len(nodes) - 1]
    print("success load model")

def unload_model():
    sess.close()

if __name__ == '__main__':
    '''
    argv:[
        port_no: flask程序运行端口号,
        model_directory: 模型所在文件夹,
        model_graph: 模型的图结构,
        input_node_name: 模型的图结构的输入节点名称,
        output_node_name: 模型的图结构的输出节点名称,
    ]
    '''
    # 参数个数不匹配
    if len(sys.argv) < 5:
        print("RETURN_CODE", 1)
        exit(1)
    port_no = -1
    try:
        port_no = int(sys.argv[1])
    except:
        # 端口值非整形
        print("RETURN_CODE", 2)
        exit(2)
    # 端口范围非BSD服务器端口范围
    if port_no < 5000 and port_no > 65535:
        print("RETURN_CODE", 3)
        exit(3)
    model_directory = sys.argv[2]
    if not os.path.exists(model_directory):
        print("RETURN_CODE", 4)
        exit(4)
    model_graph = sys.argv[3]
    if not os.path.exists(model_graph):
        print("RETURN_CODE", 5)
        exit(5)
    key = sys.argv[4]
    sess = tf.Session()
    graph = None
    try:
        input_node_name = sys.argv[5]
    except IndexError:
        input_node_name = ""
    try:
        output_node_name = sys.argv[6]
    except IndexError:
        output_node_name = ""
    load_model(model_directory, model_graph, input_node_name, output_node_name)
    try:
        model.run(host='0.0.0.0', port=port_no)
    except OSError:
        print("RETURN_CODE", 6)
        exit(6)