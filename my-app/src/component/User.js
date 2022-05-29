import React, { Component } from "react";
import './Main.css';
class User extends Component {
    constructor(props) {
        super(props);
        this.state = {
            orderId: '',
            name:'',
            inputLinkClicked:false,
        };
        this.data = []
    }

    updateInputValue(evt) {
        const val = evt.target.value;
        this.setState({
            orderId: val
        });
    }

    updateName(evt) {
        const val = evt.target.value;
        this.setState({
            name: val
        });
    }

    addUploadImage = () => {
        this.setState({inputLinkClicked:true, name:""});
    }

    uploadDetails = () => {
        //api call to upload details
        const itemsdetails = {
            data: this.data
        };

        // let h = new Headers();
        //     h.append('Content-Type', 'application/json');
        //     h.append('Access-Control-Allow-Origin', 'http://192.168.1.12:3000');
        //     h.append('Access-Control-Allow-Credentials', 'true');
        fetch('http://127.0.0.1:5000/userdetails', {
                method: 'POST',
                // headers: h,
                body : JSON.stringify(itemsdetails) ,
                })
                .then(response => response.json())
                .then(data => {
                    if (data) {
                        if (data.success) {
                            alert(data.message);
                        }
                        else {
                            alert("data not uploaded" + data.message);
                        }
                    }
                })
    }

    handleFileUpload = event => {
        //here we have image(file) and order ID
        if(this.state.orderId === ""){
            alert("Enter Order Id");
            return;
        }
        if(this.state.name === ""){
            alert("Enter Name before uploading");
            return;
        }
           alert(`${event.target.files[0].name} for order Id ${this.state.orderId}
             with name as ${this.state.name}`);
        //api call to get image url
        var myHeaders = new Headers();
        myHeaders.append("Authorization", "Client-ID 672a11f57f9ac92");

        var formdata = new FormData();
        formdata.append("image", event.target.files[0]);

        var requestOptions = {
            method: 'POST',
            headers: myHeaders,
            body: formdata,
            redirect: 'follow'
        };
    
        fetch("https://api.imgur.com/3/image/", requestOptions)
            .then(response => response.json())
            .then(result => {
                if(result.data.link === undefined){
                    alert("image hosting failed");
                    return;
                }
                var obj = {
                    orderId : this.state.orderId,
                    name : this.state.name,
                    image : result.data.link
                }
                this.data.push(obj);
                this.setState({name:''});
                alert('image uploaded successfully')
            })
            .catch(error => alert('error'+error));
    };

    render() {
        return ( 
                <div style = {{ marginTop: "300px", marginLeft: "35%", flexDirection: "column" }} >
                    <input className = "search-input mb-2"
                    type = "number"
                    onChange = { evt => this.updateInputValue(evt) }
                    placeholder = "Enter Consignment Number" />
                    <br/>
                    <div className="upload-image">
                    <div>
                <input className = "name-input"
                style = {
                    {
                        borderRadius: 10,
                        paddingVertical: 10,
                        paddingHorizontal: 10,
                        height: "40px"
                    }
                }
                type = "text"
                onChange = { evt => this.updateName(evt) }
                placeholder = "Deliver To - Name" />
                <input ref = "fileInput"
                onChange = { this.handleFileUpload }
                type = "file"
                style = {
                    { display: "none" } }
                accept = "image/*" />
                <button style = {
                    {
                        backgroundColor: "#009688",
                        borderRadius: 10,
                        paddingVertical: 10,
                        paddingHorizontal: 10,
                        width: "180px",
                        height: "40px"
                    }
                }
                onClick = {
                    () => this.refs.fileInput.click() } > Upload Image </button> 
            </div> 
            </div>
            <button className={this.state.inputLinkClicked ? "d-none" : ""} style = {
                    {
                        backgroundColor: "#39FF14",
                        width:"190px",
                        height:"40px",
                        marginLeft:"100px"
                    }
                }
                onClick={this.addUploadImage} > ADD + </button> 
            {this.state.inputLinkClicked ?
                <div>
                <input className = "name-input"
                style = {
                    {
                        borderRadius: 10,
                        paddingVertical: 10,
                        paddingHorizontal: 10,
                        height: "40px"
                    }
                }
                type = "text"
                onChange = { evt => this.updateName(evt) }
                placeholder = "Enter Name..." />
                <input ref = "fileInput"
                onChange = { this.handleFileUpload }
                type = "file"
                style = {
                    { display: "none" } }
                accept = "image/*" />
                <button style = {
                    {
                        backgroundColor: "#009688",
                        borderRadius: 10,
                        paddingVertical: 10,
                        paddingHorizontal: 10,
                        width: "180px",
                        height: "40px"
                    }
                }
                onClick = {
                    () => this.refs.fileInput.click() } > Upload Image </button> 
            </div> 
                :
                <div></div>
            }
            <button style = {
                    {
                        backgroundColor: "#39FF14",
                        width:"380px",
                        height:"40px",
                        marginTop:"5px",
                        borderRadius:"10px"
                    }
                }
                onClick={this.uploadDetails} > Submit </button> 
                <h1>{this.state.data}</h1>
            </div>
        );
    }
}
export default User;