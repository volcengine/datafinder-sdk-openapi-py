# dsl sdk使用说明
### 1. 导入
```python
from rangersdk.dsl import DSL, int_expr, string_expr, empty_expr, show
```

### 2、dsl样例以及说明
#### a. 事件查询
```python
import requests
import ujson

from rangersdk.dsl import DSL, int_expr, string_expr, empty_expr, show


dsl = (DSL.event_builder()  # 构造事件，每种类型的dsl有对应的builder                                             
       .app_id(0)  # 支持数组，这里可以是 .appid([1,2])                                                     
       .range_period('day', 1562688000, 1563206400)  # 查询时间，支持多个时间。range表示区间，有开始和结束时间，last_period 表示最近时间                      
       .range_period('hour', 1562688000, 1563206400)                        
       .group('app_channel') # 分组，支持数组，这里也可以是 .group([1,2])                                               
       .skip_cache(False) # 是否跳过缓存                                                  
       .tag({'contains_today': 0, 'show_yesterday': 0,                      
             "series_type": "line", "show_map": {}}) # 设置的标记，不参与查询条件构建，会添加到返回结果字段中                       
       .and_profile_filter(int_expr('user_is_new', '=', [0])  # 用户filter，支持and和or两种逻辑判断‘            
                           .show(1, u'老用户'))                                
       .and_profile_filter(string_expr('language', '=', ['zj_CN', 'zh_cn']) # int_exp,string_exp,empty_exp, 分别表示表达式值的内容的值类型
                           .string_expr('age', '!=', ['20'])                
                           .show(2, 'zh_CN, zh_cn; not(20)'))               
       .query(show('A', u'查询A')  # 查询指标名称, 每个query表示的是并列关系，query()方法里面的表示顺序关系                                          
              .group('app_name') # 分组，支持数组 groups([])                                           
              .event('origin', 'predefine_pageview', 'pv') # 事件描述信息                
              .measure_info('pct', 'event_index', 100) # measure_info 信息                     
              .and_filter(string_expr('os_name', '=', ['windows'])  # filter         
                          .string_expr('network_type', '!=', ['wifi'])      
                          .show('referer_label', 'referrer')))              
       .query(show('B', '查询B')                                              
              .group(['app_name'])                                          
              .event('origin', 'page_open', 'pv')                           
              .and_filter(empty_expr()                                      
                          .show('app_id_label', 'app_id')))                 
       .build()) 
                                                                  
dsl_str = ujson.dumps(dsl, indent=4)
print dsl_str

# 将dsl json化后作为body参数，进行查询
resp = requests.post(                            
    'http://ip:port/bear/api/query',                                
    data=ujson.dumps(dsl),                      
    headers={'Content-Type': 'application/json'} 
)                                                

```

#### b. 转换查询
```python
import requests
import ujson

from rangersdk.dsl import DSL, int_expr, string_expr, empty_expr, show


dsl = (DSL.funnel_builder()                                             
       .app_id(0)                                                   
       .range_period('day', 1560268800, 1562774400)                     
       .group('os_name')                                                
       .page(10, 2)                                                     
       .window('day', 10)                                               
       .skip_cache(False)                                               
       .and_profile_filter(int_expr('user_is_new', '=', [0])            
                           .string_expr('network_type', '!=', ['4g,3g'])
                           .show(1, u'老用户; not(4g, 3g)'))               
       .query(show('1', u'查询1')                                         
              .sample(100)                                             
              .event('origin', 'play_time', 'pv')                       
              .and_filter(string_expr('os_name', '=', ['windows'])      
                          .string_expr('network_type', '!=', ['wifi'])  
                          .show('referer_label', 'referrer')),          
              show('2', u'查询2')                                         
              .sample(100)                                             
              .event('origin', 'app_launch', 'pv')                      
              )                                                         
       .build())                                                        

dsl_str = ujson.dumps(dsl, indent=4)
print dsl_str

# 将dsl json化后作为body参数，进行查询
resp = requests.post(                            
    'http://ip:port/bear/api/query',                                
    data=ujson.dumps(dsl),                      
    headers={'Content-Type': 'application/json'} 
)

```

#### c. 生命周期查询
```python
import requests
import ujson

from rangersdk.dsl import DSL, int_expr, string_expr, empty_expr, show


dsl = (DSL.lifecycle_builder()                                                     
       .app_id(26142)                                                              
       .range_period('day', 1561910400, 1562428800)                                
       .page(10, 2)                                                                
       .window('day', 1)                                                           
       .skip_cache(False)                                                          
       .tag({"series_type": "line", "contains_today": 0,                           
             "metrics_type": "number", "disabled_in_dashboard": True})             
       .and_profile_filter(string_expr('custom_mp_platform', '=', ['2'])           
                           .string_expr('app_channel', 'in', ['alibaba', 'baidu']) 
                           .show(1, u'全体用户'))                                      
       .query(show('active_user', u'active_user')                                  
              .sample(100)                                                        
              .event('origin', 'app_launch', 'pv'))                                
       .build())                                                                   

dsl_str = ujson.dumps(dsl, indent=4)
print dsl_str

# 将dsl json化后作为body参数，进行查询
resp = requests.post(                            
    'http://ip:port/bear/api/query',                                
    data=ujson.dumps(dsl),                      
    headers={'Content-Type': 'application/json'} 
)

```

#### d. 用户路径查询
```python
import requests
import ujson

from rangersdk.dsl import DSL, int_expr, string_expr, empty_expr, show


dsl = (DSL.pathfind_builder()                                                
       .app_id(0)                                                        
       .range_period('day', 1563120000, 1563638400)                          
       .page(10, 2)                                                          
       .window('minute', 10)                                                 
       .skip_cache(False)                                                    
       .is_stack(False)                                                      
       .and_profile_filter(string_expr('os_name', 'in', ['android', 'ios'])  
                           .string_expr('network_type', 'in', ['wifi', '4g'])
                           .show(1, u'android, ios; wifi, 4g'))              
       .query(show('1', u'查询1')                                              
              .sample(100)                                                  
              .event('origin', 'app_launch')                                 
              .and_filter(empty_expr().show('1', u'全体用户')),                  
              show('2', u'查询2')                                              
              .sample(100)                                                  
              .event('origin', 'register')                                   
              .and_filter(empty_expr().show('1', u'全体用户')),                  
              show('3', u'查询3')                                              
              .sample(100)                                                  
              .event('origin', 'register')                                   
              .and_filter(empty_expr().show('1', u'全体用户')))                  
       .build())                                                             

dsl_str = ujson.dumps(dsl, indent=4)
print dsl_str

# 将dsl json化后作为body参数，进行查询
resp = requests.post(                            
    'http://ip:port/bear/api/query',                                
    data=ujson.dumps(dsl),                      
    headers={'Content-Type': 'application/json'} 
)

```

#### e. 留存查询
```python
import requests
import ujson

from rangersdk.dsl import DSL, int_expr, string_expr, empty_expr, show


dsl = (DSL.retention_builder()                                                         
       .app_id(0)                                                                  
       .range_period('day', 1561910400, 1563033600)                                    
       .page(10, 2)                                                                    
       .group('network_type')                                                          
       .window('day', 30)                                                              
       .skip_cache(False)                                                              
       .is_stack(False)                                                                
       .tag({"retention_from": "custom", "series_type": 'table'})                      
       .and_profile_filter(int_expr('user_is_new', '=', [0])                           
                           .show(1, u'老用户'))                                           
       .query(show('first', u'起始事件')                                                   
              .event('origin', 'page_open', 'pv')                                      
              .and_filter(string_expr('os_name', '=', ['windows', 'mac', 'ios'])       
                          .string_expr('network_type', '!=', ['4g'])                   
                          .show('os_name_label', u'os_name,network_type')),            
              show('return', u'回访事件')                                                  
              .event('origin', 'any_event')                                            
              .and_filter(string_expr('os_name', '=', ['windows', 'mac'])              
                          .string_expr('browser', '=', ['Chrome', 'Internet Explorer'])
                          .show('1', u'全体用户'))                                         
              )                                                                        
       .build())                                                                       

dsl_str = ujson.dumps(dsl, indent=4)
print dsl_str

# 将dsl json化后作为body参数，进行查询
resp = requests.post(                            
    'http://ip:port/bear/api/query',                                
    data=ujson.dumps(dsl),                      
    headers={'Content-Type': 'application/json'} 
)

```

#### f. WEB SESSION查询
```python
import requests
import ujson

from rangersdk.dsl import DSL, int_expr, string_expr, empty_expr, show


dsl = (DSL.web_builder()                                                         
       .app_id(0)                                                            
       .range_period('day', 1562774400, 1563292800)                              
       .page(10, 2)                                                              
       .group('browser')                                                         
       .web('first', 1200)                                                       
       .skip_cache(False)                                                        
       .is_stack(False)                                                          
       .tag({"contains_today": 0, "series_type": 'line'})                        
       .and_profile_filter(string_expr('os_name', '=', ['windows', 'android'])   
                           .show(1, u'操作系统'))                                    
       .query(show('session_count', u'会话数')                                      
              .sample(100)                                                      
              .event('origin', 'predefine_pageview', 'session_count')            
              .and_filter(empty_expr()                                           
                          .show('1', u'source')),                                
              show('average_session_duration', u'平均会话时长')                        
              .event('origin', 'predefine_pageview', 'average_session_duration') 
              .and_filter(empty_expr()                                           
                          .show('1', u'source')),                                
              show('bounce_rate', u'跳出率')                                        
              .event('origin', 'predefine_pageview', 'bounce_rate')              
              .and_filter(empty_expr()                                           
                          .show('1', u'source')),                                
              show('average_session_depth', u'平均会话深度')                           
              .event('origin', 'predefine_pageview', 'average_session_depth')    
              .and_filter(empty_expr()                                           
                          .show('1', u'source')))                                
       .build())                                                                 

dsl_str = ujson.dumps(dsl, indent=4)
print dsl_str

# 将dsl json化后作为body参数，进行查询
resp = requests.post(                            
    'http://ip:port/bear/api/query',                                
    data=ujson.dumps(dsl),                      
    headers={'Content-Type': 'application/json'} 
)

```

#### g. topk查询
```python
import requests
import ujson

from rangersdk.dsl import DSL, int_expr, string_expr, empty_expr, show


dsl = (DSL.topk_builder()                                                                   
       .app_id(0)                                                                       
       .range_period('day', 1563379200, 1563897600)                                         
       .order('app_version')   # 排序，默认是asc升序, 也可以链式.order('app_version','asc')                                                               
       .page(10, 2)                                                                         
       .skip_cache(True)                                                                    
       .tag({"contains_today": 0, "show_yesterday": 0, "series_type": 'line', "show_map": {}
       .and_profile_filter(int_expr('ab_version', '=', [1])                                 
                           .int_expr('user_is_new', '=', [0])                               
                           .show('B', u'新用户'))                                              
       .query(show('A', u'查询A')                                                             
              .sample(100)                                                                 
              .event('origin', 'predefine_pageview', 'pv')                                  
              .measure_info('pct', 'event_index', 100)                                      
              .and_filter(string_expr('referrer', '=',                                      
                                      ['http://www.baidu.com', 'http://www.bytedance.com'], 
                                      'event_param')                                        
                          .show('referer_label', u'referer')))                              
       .build())                                                                            
                                                                                            
dsl_str = ujson.dumps(dsl, indent=4)                                                     
print dsl_str

# 将dsl json化后作为body参数，进行查询
resp = requests.post(                            
    'http://ip:port/bear/api/query',                                
    data=ujson.dumps(dsl),                      
    headers={'Content-Type': 'application/json'} 
)
                                                                           
```

## 二、dsl client使用说明
### 1. 安装
```shell
python setup.py install
```

### 2. 导入
```python
from rangersdk.dsl import DSL, int_expr, string_expr, empty_expr, show
from rangersdk.client import RangersClient
```

### 3.使用方式
可以参考test_client.py

* 初始化 RangersClient
```python
ak = 'xxx' # ak
sk = 'xxx' # sk
bc = RangersClient(ak, sk)
```

* 调用服务
```python
bc.analysis_base('post', '/bear/api/query', body=ujson.dumps(data))
bc.analysis_base('get', '/bear/api/msg', params={'code': 'welcome'})

```


