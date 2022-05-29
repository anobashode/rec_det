import React, { Component } from 'react';
import Table from './Table';
class Deliver extends Component {
    constructor(props) {
        super(props);
        this.state = {
            orderId: '',
            flag: false,
        };
        this.names = [];
    }
    validateOrderId = () => {
        //api call to validate order ID
        fetch(`http://127.0.0.1:5000/validateOrderId?orderId=${this.state.orderId}`, {
            method: 'GET'
            })
            .then(response => response.json())
            .then(data => {
                if(data)
                {
                    if(data.success === "true"){                        
                        var dataNames = data.names.split(',');
                        var mainData = [];
                        // dataNames.array.forEach(element => {
                        //     var obj ={
                        //         name: element
                        //     }
                        //     mainData.push(obj);
                        // });
                        mainData.push(dataNames[0])
                        mainData.push(dataNames[1])
                        this.setState({flag:true});
                        //this.flag=true;
                        this.names = mainData;
                        alert(`Success: ${data.message}. please proceed with Validation`)
                    }
                    else{
                        alert(`Failed: ${data.message}`)
                    }
                }
            })
    }

    validateDelivery = () => {
        //api call to validate delivery and if confirmed show alert with message from backend
        fetch(`http://127.0.0.1:5000/validateDelivery?orderId=${this.state.orderId}`, {
            method: 'GET'
            })
            .then(response => response.json())
            .then(data => {
                if(data)
                {
                    if(data.success === "true"){
                        alert(`Success: ${data.message}. deliver package`);
                    }
                    else{
                        alert(`Failed: ${data.message}`)
                    }
                }
            })
            .catch(error => {
                alert(`ERROR: Validation Failed. please try again.` );
                console.log(error);
            })
    }

    updateInputValue(evt) {
        const val = evt.target.value;
        this.setState({
            orderId: val
        });
    }
    render() {
        return (
            <div>
            <div style = {{ marginTop: "140px", marginLeft: "40%", flexDirection: "column" }} >
                    <input className = "search-input mb-2"
                    type = "number"
                    onChange = { evt => this.updateInputValue(evt) }
                    placeholder = "Enter Consignment Number" />
                    <button style = {
                    {
                        backgroundColor: "#39FF14",
                        width:"60px",
                        height:"40px",
                        marginTop:"5px",
                        borderRadius:"10px"
                    }
                }
                onClick={this.validateOrderId} > {'>>'} </button> 
          </div>
          
          <div>
          <div>
          <button style = {
                    {
                        backgroundColor: "#39FF14",
                        width:"420px",
                        height:"50px",
                        marginTop:"30px",
                        marginLeft:"40%",
                        borderRadius:"10px"
                    }
                }
                onClick={this.validateDelivery} > Validate Delivery </button> 
          </div>
          <div>
              <Table names={this.names} />
          </div>
          </div>
          :
          <div></div>
    
          </div>
        );
    }
}
export default Deliver;