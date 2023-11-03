
const script_tag_a = function(){

    const tag_a = document.getElementsByTagName('a');

    for (let i = 0; i < tag_a.length;i++){
        tag_a[i].addEventListener('click',function(e){
            e.preventDefault();
            e.stopPropagation();
            let TAG_NAME = 'a'
            let ID = this.getAttribute("id") || ""
            let CLASS_NAME = this.getAttribute("class") || ""
            let NAME = this.getAttribute("name") || ""
            let VALUE = this.getAttribute("href")  || ""
            let CONTENT = this.textContent.replace(/[\n\t\r]/g,"").trim() || ""
            let URL = VALUE 
            let TEXT = 'Nhấn link: ' + CONTENT
            let EVENT = 'click'

            let CURRENT_URL = document.location.href

            let HOST_URL = document.location.origin
            if (URL && !URL.includes('http')){
                URL = HOST_URL +'/'+ URL
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
            console.log('a',data);
            if (CURRENT_URL.includes('accounts.google.com')){
                this.setAttribute('data_unique','my_id');
            }

            $.ajax({
                url: 'http://127.0.0.1:5000/',
                type:'POST',
                dataType: "json",
                data:data
            }
        )
    })}

};

script_tag_a();

(function() {

    let child = document.getElementsByTagName('a').length;
    setInterval(function(){
        let newChild = document.getElementsByTagName('a').length;
        if(child < newChild) {
            child = newChild;
            script_tag_a();
         }
    }, 1000);
})()
    
    