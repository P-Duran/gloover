import { Chip, makeStyles } from '@material-ui/core';
import React from 'react';
import { JobStates } from 'utils/jobUtils';

const useStyles = makeStyles({
  [JobStates.RUNNING]: {
    backgroundColor: "#e3f9dd",
    color: '#229A16',
    borderColor: '#229A16'
  },
  info: {
    backgroundColor: "#ecf6ff",
    color: '#1890FF'
  },
  [JobStates.SCHEDULED]: {
    backgroundColor: "#fff5d7",
    color: '#B78103'
  },
  [JobStates.FINISHED]: {
    backgroundColor: "#ffe1e0",
    color: '#B72136'
  },
});
export const StatusChip = ({ label, variant }) => {
  const classes = useStyles();
  return <Chip label={label} className={classes[variant]}></Chip>
}