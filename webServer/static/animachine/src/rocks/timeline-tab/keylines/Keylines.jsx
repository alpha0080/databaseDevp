import React from 'react'
import {afflatus} from 'afflatus'
import Keyline from './Keyline'
import PointerLine from './PointerLine'
import {convertTimeToPosition, getVisibleTime} from '../utils'
import {ContextMenu} from 'react-matterkit'
import union from 'lodash/union'

@afflatus
export default class Keylines extends React.Component {
  render() {
    const {timeline, actions, style} = this.props
    const height = BETON.require('config').size
    const children = []
    let pos = 0

    const renderKeyline = (keyHolder) => {
      children.push(<Keyline
        key = {keyHolder.uid}
        keyHolder = {keyHolder}
        actions = {actions}
        top = {pos}
        height = {height}/>)

      pos += height
    }

    timeline.tracks.forEach(track => {
      renderKeyline(track)
      if (track.openInTimeline) {
        track.params.forEach(param => renderKeyline(param))
      }
    })

    const menuItems = [
      {label: 'delete selected keys', onClick: () => {
        timeline.removeSelectedKeys()
      }}
    ]

    return <ContextMenu items={menuItems}>
      <div style={{...style, position: 'relative', flex: 1}}>
        {children}
        <PointerLine timeline={timeline}/>
      </div>
    </ContextMenu>
  }
}
