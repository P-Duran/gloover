import React, { useContext, useEffect, useState } from 'react';
import { Box, Checkbox, FormControlLabel, Grid, MenuItem, TextField, Toolbar, Typography } from '@material-ui/core';
import {
  makeStyles,
} from '@material-ui/core/styles';
import { capitalizeFirstLetter } from 'pages/Dashboard/Jobs/Utils';
import { GlobalContext } from 'context/GlobalContext';
import { GlooverButton } from 'components/GlooverButton';
import { scrape } from 'model/scraperApi';
import { useSnackbar } from 'notistack';
import { useHistory } from "react-router-dom";
import { DASHBOARD_PATH } from 'utils/routeUtils';
import { sleep } from 'pages/Dashboard/Jobs/Utils';

const useStylesReddit = makeStyles((theme) => ({
  root: {
    width: '100%',
    padding: "5px 15px 5px 15px",
    margin: "5px 15px 5px 15px",
    border: '0.5px solid #c2f2d7',
    overflow: 'hidden',
    borderRadius: 16,
    backgroundColor: '#fcfcfb',
    transition: theme.transitions.create(['border-color', 'box-shadow']),
    '&:hover': {
      backgroundColor: '#fff',
    },
    '&$focused': {
      backgroundColor: '#fff',
      borderColor: "#229A16",
      boxShadow: "0px 1px 10px rgba(0, 171, 85, 0.15)",
    },
  },
  focused: {},
}));

function RedditTextField(props) {
  const classes = useStylesReddit();

  return <TextField InputProps={{ classes, disableUnderline: true }} {...props} />;
}

const useStyles = makeStyles({
  paper: {
    width: "100%",
    margin: 18,
    padding: 18
  },
  tableContainer: {
    padding: 10,
    overflow: "hidden"
  }
});

export function JobCreation() {
  const classes = useStyles();
  const [formInput, setFormInput] = useState({})
  const [loading, setLoading] = useState(false)
  const { spiders } = useContext(GlobalContext);
  const { enqueueSnackbar } = useSnackbar();
  const history = useHistory();

  useEffect(() => {
    if (spiders) {
      formInput['spider_name'] = spiders[0]
    }
    formInput['trigger'] = "date"
  }, [])
  const formData = [
    { label: "url", form_name: "url", placeholder: 'Url to scrape' },
    { label: "max requests", form_name: "max_requests", placeholder: 'The number of requests the scraper will make' },
    { label: "spider name", form_name: "spider_name", placeholder: 'The name of the spider that will scrape the url', select: true, options: spiders },
    { label: "trigger", form_name: "trigger", placeholder: 'The type of the trigger that will start the scraper', select: true, options: ["date", "interval"] },
    { label: "trigger option", form_name: "trigger_option", placeholder: '' }
  ]

  const handleInputCheckBox = evt => {

    setFormInput({ ...formInput, [evt.target.name]: evt.target.checked });
  }
  const handleInput = evt => {
    const name = evt.target.name;
    const newValue = evt.target.value;
    setFormInput({ ...formInput, [name]: newValue });
  };
  const handleDefaultValue = (data) => {
    return data.options ? data.options[0] : ""
  }
  return (
    <Grid container direction='column' className={classes.paper}>
      <Box boxShadow={3} borderRadius={16} padding={2}>
        <Toolbar style={{ marginBottom: 10 }}>
          <Typography variant="h6" id="tableTitle" component="div">
            Create a new Job
          </Typography>
        </Toolbar>
        <form onSubmit={"handleSubmit"}>
          <Grid container justify='space-between' alignItems='stretch' >
            {[...formData.map(data =>
              <Grid key={data.label} item xs={6} style={{ paddingBottom: 20, minWidth: 200 }}>
                <Typography variant='subtitle2' style={{ marginLeft: 20 }}>{capitalizeFirstLetter(data.label)}</Typography>
                <RedditTextField
                  name={data.form_name}
                  value={data.form_name in formInput ? formInput[data.form_name] : handleDefaultValue(data)}
                  placeholder={data.placeholder}
                  select={data?.select}
                  onChange={handleInput}
                >{data.options && data.options.map((option) => (
                  <MenuItem key={option} value={option}>
                    {option}
                  </MenuItem>
                ))}</RedditTextField>
              </Grid>),
            <Grid key="test" item xs={12} style={{ paddingBottom: 20, minWidth: 200, marginLeft: 20 }}>
              <FormControlLabel
                control={<Checkbox checked={"test" in formInput ? formInput["test"] : false} onChange={handleInputCheckBox} name="test" style={{ color: '#4d4d4d' }} />}
                label="Test Job" />
            </Grid>
            ]}
          </Grid>
        </form>
      </Box>
      <Grid item container justify='flex-end'>
        <GlooverButton
          label='Submit'
          variant='secondary'
          loading={loading}
          onClick={async () => {
            setLoading(true);
            await sleep(1500)
            scrape(formInput)
              .then(data => {
                setLoading(false);
                history.push(DASHBOARD_PATH);
                enqueueSnackbar(`Job "${data.items.name}" was created correctly`, {
                  variant: 'success',
                  autoHideDuration: 3000,
                })
              })
              .catch(e => {
                setLoading(false);
                enqueueSnackbar(e.toString(), {
                  variant: 'error',
                  autoHideDuration: 3000,
                })
              })
          }}>
        </GlooverButton>
      </Grid>
    </Grid>
  );
}