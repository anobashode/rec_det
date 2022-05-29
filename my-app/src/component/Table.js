import React, { Component } from 'react';
class Table extends Component {
    constructor(props) {
        super(props);
        this.state = {
            orderId: '',
            data: this.props.names
        };
    }
render(){
    return(
        <div className="App">
      <table>
        <tr>
          <th>Consignee Name</th>
        </tr>
        {this.state.data.map((val, key) => {
          return (
            <tr key={key}>
              <td>{val.name}</td>
            </tr>
          )
        })}
      </table>
    </div>
    );
}
}
export default Table;