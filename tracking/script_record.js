var script_embb = document.createElement('div');
script_embb.id = 'myscript';
script_embb.hidden = 'hidden';
document.getElementsByTagName('body')[0].appendChild(script_embb);


const script_record_tag_a = function(){
    const tag_a = document.getElementsByTagName('a');

    for (let i = 0; i < tag_a.length;i++){
        tag_a[i].setAttribute("target", "_self")
    }
};

script_record_tag_a();

(function() {

    var child = document.getElementsByTagName('a').length;
    i=1
    setInterval(function(){
        var newChild = document.getElementsByTagName('a').length;

        if(child < newChild ) {
           child = newChild;
           script_record_tag_a(i);
           i+=1
        }
        
    }, 500);

})()


