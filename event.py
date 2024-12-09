import dictionary

def event_resalt(signal):
    new_tool = dictionary.item_dict[signal][0]
    lost_tool = dictionary.item_dict[signal][1]
    extra_event_boo = dictionary.item_dict[signal][2]
    return new_tool, lost_tool, extra_event_boo

def call_text(signal):
    with open(dictionary.text_dict[signal],'r',encoding='utf-8') as f:
        text = f.read()
    return text