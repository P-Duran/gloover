import { ButtonBase, CircularProgress, fade, Grow, makeStyles, Typography } from '@material-ui/core';
import React from 'react';
const useStyles = makeStyles((theme) => ({
  primary: {
    backgroundColor: '#00AB55',
    minHeight: "40px",
    minWidth: '120px',
    borderRadius: 12,
    padding: "7px 25px 7px 25px",
    color: props => fade("#ffffff", props.loading ? 0.3 : 1),
    boxShadow: "0px 1px 10px rgba(0, 171, 85, 0.25)",
    margin: 10,
  },
  secondary: {
    backgroundColor: '#FFC107',
    minHeight: "40px",
    minWidth: '120px',
    borderRadius: 12,
    padding: "7px 25px 7px 25px",
    color: props => fade("#000000", props.loading ? 0.3 : 1),
    boxShadow: "0px 1px 10px rgba(255, 193, 7, 0.25)",
    margin: 10,
  },
  destructive: {
    backgroundColor: '#ff4842',
    minHeight: "40px",
    minWidth: '120px',
    borderRadius: 12,
    padding: "7px 25px 7px 25px",
    color: props => fade("#ffffff", props.loading ? 0.3 : 1),
    boxShadow: "0px 1px 10px rgba(255, 72, 66, 0.25)",
    margin: 10,
  },
  text: {

    color: 'white'

  }
}));

export function GlooverButton({ label = "Button", variant = 'primary', onClick = () => { }, loading = false }) {
  const classes = useStyles({loading});
  return <ButtonBase className={classes[variant]} onClick={onClick}>

    <Grow in={loading} unmountOnExit>
      <CircularProgress size={25} style={{ color: 'black', position: 'absolute' }} />
    </Grow>
    <Typography variant='subtitle1'>
      {label}
    </Typography>
  </ButtonBase>
}