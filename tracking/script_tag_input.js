
const script_tag_input = function() {

    const tag_input = document.getElementsByTagName('input');
    const tag_textarea = document.getElementsByTagName('textarea');

    let list_input_click = ['submit','radio','checkbox','file','image','reset']

    for (let i = 0; i < tag_input.length;i++) {
        let TYPE = tag_input[i].getAttribute('type')

        if (list_input_click.includes(TYPE)) {
            tag_input[i].addEventListener('click',function(e){
                e.stopPropagation();
                
                let TAG_NAME = 'input'
                let ID = this.getAttribute("id") || ""
                let CLASS_NAME = this.getAttribute("class") || ""
                let NAME = this.getAttribute("name") || ""
                let VALUE = this.value  || ""
                let CONTENT = this.textContent || ""
                let URL = this.getAttribute("href") || ""
                let TEXT = 'Nhấn nút: '
                let EVENT = 'click'
                let CURRENT_URL = document.location.href
                let HOST_URL = document.location.origin
                if (URL && !URL.includes('http')){
                    URL = HOST_URL + URL
                }
                let TEXT_FROM_PARENT = this.parentElement.innerText.toLowerCase().replace(/[\n\t\r]/g,"").trim() 

                TEXT += VALUE ? VALUE : TEXT_FROM_PARENT

                
                let data  = {
                    TAG_NAME:TAG_NAME,
                    ID:ID,
                    CLASS_NAME:CLASS_NAME,
                    NAME:NAME,
                    VALUE:VALUE,
                    CONTENT:CONTENT,
                    TEXT:TEXT,
                    EVENT:EVENT,
                    URL:URL
                }
        
                data = JSON.stringify({'URL':URL, 'ACTION':data, 'WINDOW_ID':`${window}`,'CURRENT_URL':CURRENT_URL});
                if (CURRENT_URL.includes('accounts.google.com')){
                    this.setAttribute('data_unique','my_id');
                }
    
                $.ajax({
                    url: 'http://127.0.0.1:5000/',
                    type:'POST',
                    dataType: "json",
                    data:data
                })
            })
        }
        else {
            let input_dict = {}

            tag_input[i].addEventListener('focusout',function(e){
                let TAG_NAME = 'input'
                let ID = this.getAttribute("id") || ""
                let CLASS_NAME = this.getAttribute("class") || ""
                let NAME = this.getAttribute("name") || ""
                let VALUE = this.value  || ""
                let CONTENT = this.textContent || ""
                let URL = this.getAttribute("href") || ""
                let PLACEHOLDER = this.getAttribute("placeholder") || ""
                let TEXT = 'Nhập '+ PLACEHOLDER.toLowerCase().replace(/[\n\t\r]/g,"").trim() + ': '+ VALUE
                let EVENT = 'input'
                let HOST_URL = document.location.origin
                let CURRENT_URL = document.location.href
                if (URL && !URL.includes('http')){
                    URL = HOST_URL + URL
                }
        
                let data  = {
                    TAG_NAME:TAG_NAME,
                    ID:ID,
                    CLASS_NAME:CLASS_NAME,
                    NAME:NAME,
                    VALUE:VALUE,
                    CONTENT:CONTENT,
                    TEXT:TEXT,
                    EVENT:EVENT,
                }
                data = JSON.stringify({'URL':URL, 'ACTION':data, 'WINDOW_ID':`${window}`,'CURRENT_URL':CURRENT_URL});
                
                if (VALUE!=='' && input_dict[i] !== VALUE){
                    input_dict[i] = VALUE
                    if (CURRENT_URL.includes('accounts.google.com')){
                        this.setAttribute('data_unique','my_id');
                    }
        
                    $.ajax({
                        url: 'http://127.0.0.1:5000/',
                        type:'POST',
                        dataType: "json",
                        data:data
                    })
                }
            })
    }}


};


script_tag_input();

(function() {

    let child = document.getElementsByTagName('input').length;
    setInterval(function(){
        let newChild = document.getElementsByTagName('input').length;
        if(child < newChild) {
            child = newChild;
            script_tag_input();
         }
    }, 1000);
})()
    
    