
const script_tag_textarea = function() {

    const tag_textarea = document.getElementsByTagName('textarea');

    for (let i = 0; i < tag_textarea.length;i++) {
        let input_dict = {}

        tag_textarea[i].addEventListener('focusout',function(e){
            e.stopPropagation();
            let TAG_NAME = 'textarea';
            let ID = this.getAttribute("id") || ""
            let CLASS_NAME = this.getAttribute("class") || ""
            let NAME = this.getAttribute("name") || ""
            let VALUE = this.value  || ""
            let CONTENT = this.textContent || ""
            let URL = this.getAttribute("href") || ""
            let PLACEHOLDER = this.getAttribute("placeholder") || ""
            let TEXT = 'Nhập '+ PLACEHOLDER.toLowerCase().replace(/[\n\t\r]/g,"").trim() + ': '+ VALUE
            let EVENT = 'input'
            let CURRENT_URL = document.location.href
            let HOST_URL = document.location.origin
            console.log(VALUE,'textarea')
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
                    this.setAttribute('id','my_id');
                }
    
                $.ajax({
                    url: 'http://127.0.0.1:5000/',
                    type:'POST',
                    dataType: "json",
                    data:data
                })
        }})
    }
};


script_tag_textarea();

(function() {

    let child = document.getElementsByTagName('textarea').length;
    setInterval(function(){
        let newChild = document.getElementsByTagName('textarea').length;
        if(child < newChild) {
            child = newChild;
            script_tag_textarea();
         }
    }, 1000);
})()
    
    