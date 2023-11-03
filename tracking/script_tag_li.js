
const script_tag_li = function() {

    const tag_li = document.getElementsByTagName('li');
    const tag_exp= ['img','span','div','svg','path','form']
    for (let i = 0; i < tag_li.length;i++){
        tag_li[i].addEventListener('click',function(e){
            number_of_child = tag_li[i].getElementsByTagName('*').length
            for (tag of tag_exp){
                number_of_child -= tag_li[i].getElementsByTagName(tag).length;
            }
            if (number_of_child > 0 ){
                return 
            }

            let TAG_NAME = 'li'
            let ID = this.getAttribute("id") || ""
            let CLASS_NAME = this.getAttribute("class") || ""
            let NAME = this.getAttribute("name") || ""
            let VALUE = this.value  || ""
            let CONTENT = this.textContent || ""
            let URL = this.getAttribute("href") || ""
            let TEXT = 'Chọn mục: '+ CONTENT.replace(/[\n\t\r]/g,"").trim()
            let EVENT = 'click'
            let CURRENT_URL = document.location.href
            let HOST_URL = document.location.origin
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

script_tag_li();


(function() {

    let child = document.getElementsByTagName('li').length;
    setInterval(function(){
        let newChild = document.getElementsByTagName('li').length;
        if(child < newChild) {
            child = newChild;
            script_tag_li();
         }
    }, 1000);
})()

