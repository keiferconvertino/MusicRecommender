import React, {useState,useEffect} from 'react';

import { TextField, Button, Grid, Item, Select, MenuItem, InputLabel, FormControl } from '@mui/material';


function About() {
    return (
        <div className = "about">
            <h1>About</h1>
            <p className = "about">This application was built to help music listeners find music similar to the songs that they love, and to help music creators predict the success of their songs and learn how they can make them more popular!</p>
            <h1>User Guide</h1>
            <p className = "about">Select the "Listeners" tab to get music recommendations. All you need to do is specify a song you like, the category of songs you want to receive recommendations from, and how many recommendations you want!</p>
            <p className = "about">Select the "Artists" tab to get a popularity prediction for your song, and compare your song to other popular songs of the category you choose!</p>
            <h1>About Us</h1>
            <p className = "about">This website and all machine learning models were built by Irpan Yierpan (Rice '23) and Keifer Convertino (Rice '22) for our class DSCI 303 (Machine Learning).</p>
            
        </div>
    )
}

export default About
