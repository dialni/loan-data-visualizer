import './DataPanel.css'

function RedGreenMarker(val) {
  if (val > 0){return "#62db39"} 
  else if (val < 0) {return "#d03520"}
  else {return "#f0f1f3"}
}

export default function DataPanel({title, datadict}) {
  return (
    <div className='DataPanel'>
			<h3>{title}</h3>
			<div>
				{
          datadict.map((o, index) => {
            return (
							<div key={index} className='DataPanelRow'>
								<h4>{o[0]}: <span style={{color: RedGreenMarker(o[1])}}>{o[1].toLocaleString("en-US") + o[2]}</span></h4>
								{}
							</div>
            );
          })
        }
			</div>
    </div>
  )
}