import React from 'react';
import InputBase from '@material-ui/core/InputBase';
import { Box, Chip } from '@material-ui/core';

export const InputText = ({ label = 'label', placeholder = "placeholder", onChange = (e) => { } }) => {
  return <Box m={1}>
    <Chip
      icon={<Chip label={label} style={{minWidth: 70}}></Chip>}
      label={
        <InputBase
          placeholder={placeholder}
          onChange={onChange}
          style={{width: 400}}
        ></InputBase>
      }
      style={{ backgroundColor: '#f2f2f2', maxWidth: 600}}
    ></Chip>
  </Box>
}