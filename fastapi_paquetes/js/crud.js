var app=new Vue({
    el: '#app',
    data: {
        message:'Historial Envios',
        info:[]
    },
    mounted(){
      axios.get("http://127.0.0.1:8000/").then(respuesta=>this.info=respuesta.data)
       }
})

