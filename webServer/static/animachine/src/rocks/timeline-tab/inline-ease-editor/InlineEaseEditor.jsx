import React from 'react'
import {afflatus} from 'afflatus'
import ControlPoint from './ControlPoint'
import {convertTimeToPosition} from '../utils'
import ClickAway from 'react-matterkit/lib/utils/ClickAway'

@afflatus
export default class InlineEaseEditor extends React.Component {
  static propTypes = {
    timeline: React.PropTypes.object,
    actions: React.PropTypes.object,
  }

  handleClickAway = () => {
    // const {actions, timeline} = this.props
    // if (timeline.inlineEaseEditor) {
    //   actions.setInlineEaseEditorOfTimeline({
    //     timelineId: timeline.id,
    //     inlineEaseEditor: false,
    //   })
    // }
  }

  render() {
    const {timeline, dividerPos, scrollPosition, actions} = this.props
    const {inlineEaseEditor} = timeline
    if (
      !inlineEaseEditor
      || !inlineEaseEditor.targetKey
      || !inlineEaseEditor.targetKey.firstParent //HACK: fix if the key was removed
    ) {
      return <div hidden/>
    }
    const {top, height, targetKey} = inlineEaseEditor
    const keyPosition = targetKey.parent('Param').keyTimes.indexOf(targetKey.time)
    if (keyPosition === 0) {
      return <div hidden/>
    }
    const previousKeyTime = targetKey.parent('Param').keyTimes[keyPosition - 1]
    const startTime = previousKeyTime
    const endTime = targetKey.time
    const left = convertTimeToPosition(timeline, startTime)
    const right = convertTimeToPosition(timeline, endTime)
    const width = right - left

    const rootStyle = {
      position: 'absolute',
      left: left + dividerPos,
      top: (top + height * 2) - scrollPosition,
      transform: 'scaleY(-1)',
      pointerEvents: 'none',
    }
    const rootSvgStyle = {
      position: 'absolute',
      top: '0px',
      left: '0px',
      overflow: 'visible',
    }

    function renderPath(w, h) {
      const {
        pointAX: pax,
        pointAY: pay,
        pointBX: pbx,
        pointBY: pby,
      } = targetKey.ease

      const d = [
        `M${w*pax},${h*pay}`,
        `L0,0`,
        `C${w*pax},${h*pay} ${w*pbx},${h*pby} ${w},${h}`,
        `L${w*pbx},${h*pby}`
      ].join(' ')

      const style = {
        fill: 'none',
        stroke: '#00BFFF',
      }

      return <path {...{d, style}}/>
    }

    function renderControlPoint(pointName, spaceX, spaceY) {
      const {controlledEases} = timeline.inlineEaseEditor
      const controlEase = targetKey.ease
      const x = controlEase[`point${pointName}X`]
      const y = controlEase[`point${pointName}Y`]

      return <ControlPoint
        {...{x, y, spaceX, spaceY, history: timeline.history}}
        onChange = {({x, y}) => {
          controlledEases.forEach(ease => {
            ease[`setPoint${pointName}X`](x)
            ease[`setPoint${pointName}Y`](y)
          })
        }}/>
    }

    return <ClickAway onClickAway={this.handleClickAway}>
      <div style={rootStyle}>
        <svg style={rootSvgStyle}>
          {renderPath(width, height)}
        </svg>
        {renderControlPoint('A', width, height)}
        {renderControlPoint('B', width, height)}
      </div>
    </ClickAway>
  }
}
