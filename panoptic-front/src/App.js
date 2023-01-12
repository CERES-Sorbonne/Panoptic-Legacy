import React from 'react';
import './App.css'
import {ROOT_URL} from './utils/const'

function App() {
  // define a state variable to store the images
  const [clusters, setClusters] = React.useState([]);
  const [page, setPage] = React.useState(1);
  const [imageSize, setImageSize] = React.useState(200);
  const [sensibility, setSensibility] = React.useState(2);
  const [selectedImage, setSelectedImage] = React.useState(-1)
  let [similarView, setSimilarView] = React.useState(-1)
  
  // use the React useEffect hook to fetch the images from the server when the component mounts
  React.useEffect(() => {
    console.log("toto")
    fetch(ROOT_URL + '/images/')
      .then(response => response.json())
      .then(data => setClusters(data));
  }, []);


  const handleClickOnImage = (image) => {
    if(image === selectedImage){
      if(similarView !== image){
        fetch(ROOT_URL + '/images/similar/' + image.split('/')[2])
        .then(response => response.json())
        .then(data => setClusters(data));
        setSimilarView(image);
        window.scrollTo(0, 0)
      }
      else{
        fetch(ROOT_URL + '/images/')
        .then(response => response.json())
        .then(data => setClusters(data));
        setSimilarView(-1);
        setSelectedImage(-1);
      }
    }
    else{
      setSelectedImage(image)
    }
  }
  const getClusters= () => {
    fetch(ROOT_URL + '/clusters/')
        .then(response => response.json())
        .then(data => setClusters(data));
  }
  let css = "repeat(auto-fit, minmax(" + imageSize + "px," + imageSize + "px)"
  // render the images
  return (
    
    <div className="main">
      <header className="control" style={{color: 'white'}}>
        <input type="range" min="0" max="500" step="20" value={imageSize} onChange={(e) => setImageSize(e.target.value)} />
        <span>{imageSize}px</span>
        <button style={{marginLeft: "0.5rem"}} onClick={() => getClusters()}>Make Clusters</button>
        {similarView !== -1 && 
          (<div style={{display: "inline-block"}}>
            <input type="range" min="0.1" max="20" step="0.1" value={sensibility} onChange={(e) => setSensibility(e.target.value)}/>
            <span>{100 - (sensibility * 5)}%</span>
          </div>)}
      </header>
      {clusters.map((images, index) => 
        (<div className="cluster">
          <h1>{similarView === -1 ? 
            (clusters.length === 1 ? 
            "Toutes les images " : "Cluster " + index) + "(" + images.length + " images )" 
            : "Images similaires à " + similarView + "(" + images.filter(i => i.dist <= sensibility).length + " images )"}</h1>
          {/* <h1>Cluster {index} ({!similarView ? images.length : images.filter(i => i.dist <= sensibility).length} images)</h1> */}
          <div className="image-mosaic" style={{gridTemplateColumns: css, gridAutoRows: imageSize + "px"}}>
            {images.slice(0, 100 * page).map((image, key) => (
              image.dist === null || image.dist <= sensibility ?
              <Image image={image.name} selected={selectedImage === image.name} key={key} dist={key !== 0 ? image.dist : null} onClick={() => handleClickOnImage(image.name)}/>
              : ""
            ))}
            <button onClick={() => setPage(page + 1)}>Load More</button>
          </div>
        </div>))
      }
    </div>
  );
}

const Image = ({image, selected, onClick, dist}) => {
  return (
    <div className={"card" + (selected ? " wide tall" : "")} 
    style={{backgroundImage: 'url(' + ROOT_URL + image + ')'}} 
    onClick={onClick}>
      {dist !== null && <span className="dist">{(100 - (dist * 5)).toFixed(2)}</span>}
    </div>
  )
}
export default App;