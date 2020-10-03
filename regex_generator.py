def csstoRegex(css_selector, result_type = 'innerHTML'):
    pos_class = css_selector.find('.')
    pos_id = css_selector.find('#')
    pos_other_attributes = css_selector.find('[')

    regex = ''
    if pos_class != -1 or pos_id != -1 or pos_other_attributes != -1:
        d = {'id': pos_class, 'class': pos_id, 'other': pos_other_attributes}
        d = {key: d[key] for key in d if d[key]>0}
        key_min = min(d.keys(), key=(lambda k: d[k]))
        val = d[key_min]
        tagname = css_selector[:val]
        regex = '<' + tagname + '\\s*'
        while len(d)>0:
            d.pop(key_min)
            if len(d) > 0: #more than one attribute, the ordering of attributes is a crucial case for regex
                temp_key_min = min(d.keys(), key=(lambda k: d[k]))
                temp_val = d[temp_key_min]
                if key_min == 'id':
                    regex += 'class=\\s*?[\'|"][\\sa-zA-Z0-9_]*?' + css_selector[val+1:temp_val].replace('.', '[\\sa-zA-Z0-9_]*?') + '[\\sa-zA-Z0-9_]*?[\'|"]\\s*?'
                elif key_min == 'class':
                    regex += 'id=\\s*?[\'|"][\\sa-zA-Z0-9_]*?' + css_selector[val+1:temp_val].replace('.', '[\\sa-zA-Z0-9_]*?') + '[\\sa-zA-Z0-9_]*?[\'|"]\\s*?'
                else:
                    regex += css_selector[val+1:val+1+css_selector[val+1:].find(']')].replace('"', '\\s*?[\'|"]').replace('\'', '\\s*?[\'|"]')      
                key_min = temp_key_min
                val = temp_val
            else:
                if key_min == 'id':
                    regex += 'class=\\s*?[\'|"][\\sa-zA-Z0-9_]*?' + css_selector[val+1:].replace('.', '[\\sa-zA-Z0-9_]*?') + '[\\sa-zA-Z0-9_]*?[\'|"]\\s*?'
                elif key_min == 'class':
                    regex += 'id=\\s*?[\'|"][\\sa-zA-Z0-9_]*?' + css_selector[val+1:].replace('.', '[\\sa-zA-Z0-9_]*?') + '[\\sa-zA-Z0-9_]*?[\'|"]\\s*?'
                else:
                    regex += css_selector[val+1:val+1+css_selector[val+1:].find(']')].replace('"', '\\s*?[\'|"]').replace('\'', '\\s*?[\'|"]')
        
        if result_type == 'outerHTML':
            regex += '>.*?</' + tagname + '>'
        elif result_type == 'HTMLtag':
            regex += '>'
        else:
            regex += '>(.*?)</' + tagname + '>'
    else: #means css_selector only contains tag name
        if result_type == 'outerHTML':
            regex = '<' + css_selector + '>.*?</' + css_selector + '>'
        elif result_type == 'HTMLtag':
            regex = '<' + css_selector + '>'
        else:
            regex = '<' + css_selector + '>(.*?)</' + css_selector + '>'

    return regex

def ahreftoRegex(css_selector):
    if len(css_selector)>=0:
        if css_selector[0] != 'a':
            return ''
        else:
            temp = csstoRegex(css_selector, 'HTMLtag')
            end_pos = temp.find('>')  
            return temp[:end_pos] + '[\\sa-zA-Z0-9_]*?href=\\s*?[\'|"](.*?)[\'|"][\\sa-zA-Z0-9_]*?>'
    else: 
        return ''