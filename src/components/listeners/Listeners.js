import React, {useState,useEffect} from 'react';

import { TextField, Button, Grid, Item, Select, MenuItem, InputLabel, FormControl } from '@mui/material';


function Listeners() {

    const [category,setCategory] = useState(0)

    const [recommendedSongs,setRecommendedSongs] = useState([])
    const [songsFetched,setSongsFetched] = useState(false)
    const [search, setSearch] = useState([])
    const [numRecs, setNumRecs] = useState(3)


    const handleClick = async() => {


        fetch('/backend/getRecommendations?songName='+search+"&category="+category+"&numRecs="+numRecs)
        .then(res => res.json()).then(res => {
            setRecommendedSongs(res.recommendations)
            setSearch(res.name + ' - ' + res.artist)
            setSongsFetched(true)
            console.log(res)
        })
    }


    function handleCatChange(e) {
        setCategory(e.target.value)
    }


    function handleSearchChange(e) {
        setSearch(e.target.value)
    }

    function handleNumRecsChange(e) {
        setNumRecs(e.target.value)
    }

    return (
      <div>
          <h1 className="listenersHeader"> Listeners </h1>
          <div className="songSearch">
            
            <h2>Enter a Song You Like and a Category for Recommendations!</h2>


            <div className="songInput"> 
            {/* <Grid className = "input" container spacing = {2}> */}
                {/* <Grid className="d-flex" item xs > */}
                    <div className = "songNameInput">
                        <TextField label = "Enter a Song" id="outlined-basic" onChange={handleSearchChange} value={search} marginRight="2px" color ="success" variant="outlined" />

                    </div>
                    <div className = "numRecsInput">
                        <TextField label = "# of Recs" id="outlined-basic" onChange={handleNumRecsChange} value={numRecs} stylee = {{ marginLeft: 2, width: 30, marginRight : 2}} color ="success" variant="outlined" />

                    </div>

                {/* </Grid> */}
                {/* <Grid  className="d-flex" marginLeft="2px" item xs> */}
                    <FormControl>
                    <InputLabel color= "success" id="demo-simple-select-label">Category</InputLabel>
                    <Select
                        style={{minWidth: 130, marginLeft: 10}}
                        labelId="demo-simple-select-label"
                        id="demo-simple-select"
                        value={category}
                        onChange={handleCatChange}
                        color = "success"
                        label= "Category"
                        defa
                    >
                        <MenuItem value={0}>All</MenuItem>
                        <MenuItem value={1}>Acoustic</MenuItem>
                        <MenuItem value={2}>Chill</MenuItem>
                        <MenuItem value={3}>Dance</MenuItem>
                        <MenuItem value={4}>Happy</MenuItem>
                        <MenuItem value={5}>Loud</MenuItem>
                        <MenuItem value={6}>A Capella</MenuItem>
                        <MenuItem value={7}>Alternative</MenuItem>
                        <MenuItem value={8}>Blues</MenuItem>
                        <MenuItem value={9}>Classical</MenuItem>
                        <MenuItem value={10}>Country</MenuItem>
                        <MenuItem value={11}>Dance</MenuItem>
                        <MenuItem value={12}>Electronic</MenuItem>
                        <MenuItem value={13}>Folk</MenuItem>
                        <MenuItem value={14}>Hip-Hop</MenuItem>
                        <MenuItem value={15}>Indie</MenuItem>
                        <MenuItem value={16}>Jazz</MenuItem>
                        <MenuItem value={17}>Movie</MenuItem>
                        <MenuItem value={18}>Opera</MenuItem>
                        <MenuItem value={19}>Pop</MenuItem>
                        <MenuItem value={20}>RnB</MenuItem>
                        <MenuItem value={21}>Rap</MenuItem>
                        <MenuItem value={22}>Reggae</MenuItem>
                        <MenuItem value={23}>Reggaeton</MenuItem>
                        <MenuItem value={24}>Rock</MenuItem>
                        <MenuItem value={25}>Ska</MenuItem>
                        <MenuItem value={26}>Soul</MenuItem>
                        <MenuItem value={27}>Soundtrack</MenuItem>
                        <MenuItem value={28}>World</MenuItem>
                    </Select>
                    </FormControl>
                    <Button className = "inputSongSearch" onClick= {handleClick} variant="contained" color = "success">Get Similar Songs</Button>
                {/* </Grid>
            </Grid> */}

            </div>
          </div>
          <div className="recommendedSongs">
              {songsFetched && (
                  <div>
                      <h3>Our Recommendations:</h3>
                    {recommendedSongs.map((recommendation,i) => {
                        return (
                            <div className = 'songRecommendation'>
                                <a href = {recommendation.url}>{recommendation.name + " - " + recommendation.artist}</a>
                                <img className = 'albumCover' alt ='' src = {recommendation.cover}></img>
                            </div>
                        )
                    })}
                  </div>
              )}
          </div>
      </div>
    );
  }
  
  export default Listeners;
  