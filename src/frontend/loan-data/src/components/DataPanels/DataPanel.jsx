import './DataPanel.css'

function RedGreenMarker(val, normalColor) {
  if (normalColor === 'green') {
    if (val > 0){return "#52d154"} 
      else if (val < 0) {return "#d84219"}
      else {return "#f0f1f3"}
  } else {
    if (val > 0){return "#d84219"} 
      else if (val < 0) {return "#52d154"}
      else {return "#f0f1f3"}
  }
}

export default function DataPanel({row1, row2}) {
  return (
    <div className='DataPanel'>
      
      <div className='DataPanelTitleRow'>
        <p>{row1['title']}</p>
        <p style={{color: RedGreenMarker(row1['tval'], row1['tvalc'])}}>{row1['tval'] + '%'}</p>
      </div>
			<h3>{row1['valu'] === 'USD' && '$'}{row1['val'].toLocaleString('en-US')}{row1['valu'] === '%' && '%'}</h3>
      
      <div className='DataPanelLineBreak' />
      
      <div className='DataPanelTitleRow'>
        <p>{row2['title']}</p>
        <p style={{color: RedGreenMarker(row2['tval'], row2['tvalc'])}}>{row2['tval'] + '%'}</p>
      </div>
			<h3>{row2['valu'] === 'USD' && '$'}{row2['val'].toLocaleString('en-US')}{row2['valu'] === '%' && '%'}</h3>
    </div>
  )
}