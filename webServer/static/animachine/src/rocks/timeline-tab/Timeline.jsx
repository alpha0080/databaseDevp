import React, {PropTypes} from 'react'
import {afflatus} from 'afflatus'
import ReactDOM from 'react-dom'
import Controls from './controls/Controls'
import Keylines from './keylines/Keylines'
import Timebar from './timebar/Timebar'
import Toolbar from './toolbar/Toolbar'
import DividerLine from './DividerLine'
import customDrag from 'custom-drag'
import {HotKeys} from 'react-hotkeys'
import hotkeyMap from './hotkeyMap'
import {Scrollable, getTheme} from 'react-matterkit'
import InlineEaseEditor from './inline-ease-editor/InlineEaseEditor'

function preventInputFireEvent(run) {
  return (event) => {
    if (event.path[0].localName !== 'input') {
      event.preventDefault()
      run(event)
    }
  }
}

function preventPropagation(run) {
  return (event) => {
    if (event.keyCode === 8) {
      // event.preventDefault()
      run(event)
    }
  }
}

function handlerWrapperPreventInputFireEvent(handler) {
  const newHandler = {}
  for (var key in handler) {
    if (handler.hasOwnProperty(key)) {
      newHandler[key] = preventPropagation(preventInputFireEvent(handler[key]))
    }
  }
  return newHandler
}

const dragOptions = {
  onDown(props, monitor, component) {
    monitor.setData({
      initDividerPos: component.state.dividerPos
    })
  },
  onDrag(props, monitor, component) {
    const offset = monitor.getDifferenceFromInitialOffset().x
    const {initDividerPos} = monitor.data
    component.setState({dividerPos: initDividerPos + offset})
  }
}

@customDrag(dragOptions, connect => ({
  dragRef: connect.getDragRef()
}))
@afflatus
export default class Timeline extends React.Component {
  static propTypes = {
    timeline: PropTypes.object,
    headHeight: PropTypes.number,
  }

  static defaultProps = {
    headHeight: 21
  }

  constructor(props) {
    super(props)
    this.state = {
      dividerPos: 300,
      fullWidth: 2000,
      scrollPosition: 0
    }
  }

  componentDidMount() {
    this.testOwnSize()
    this._testOwnSizeSetI = setInterval(() => this.testOwnSize(), 312)
  }


  componentWillUnmount() {
    clearInterval(this._testOwnSizeSetI)
  }

  testOwnSize = () => {
    const {width: nodeWidth} = ReactDOM.findDOMNode(this).getBoundingClientRect()
    const {dividerPos, fullWidth} = this.state
    const {state, actions} = BETON.require('project-manager')
    const timeline = state.currentTimeline

    if (nodeWidth !== fullWidth) {
      this.setState({fullWidth: nodeWidth})
    }

    const timelineWidth = nodeWidth - dividerPos
    if (timeline && timeline.width !== timelineWidth) {
      actions.set(timeline, 'width', timelineWidth)
    }
  }

  handleChangeScrollPosition = (scroll) => {
    this.setState({scrollPosition: scroll})
  }

  render() {
    const {state, actions} = BETON.require('project-manager')
    const timeline = state.currentTimeline

    if (!timeline) {
      return <div hidden/>
    }

    const {
      dividerPos,
      fullWidth,
      scrollPosition
    } = this.state
    const {
      headHeight,
      dragRef
    } = this.props
    const colors = getTheme(this).getStyle('colors')
    const rootStyle = {
      backgroundColor: colors.grey4,
      display: 'flex',
      flexDirection: 'column',
      flex: 1,
    }

    const hotkeyHandlers = handlerWrapperPreventInputFireEvent({
      delete() {
        timeline.removeSelectedKeys()
      },
      undo() {timeline.history.undo()},
      redo() {timeline.history.redo()},
    })
    const commonProps = {timeline, actions}

    return <HotKeys
        keyMap = {hotkeyMap}
        handlers = {hotkeyHandlers}
        style={{outline: 0, flex: 1, display: 'flex', pointerEvents: 'auto', overflow: 'hidden'}}>
      <div style={rootStyle}>
        <div style={{
          display: 'flex',
          height: headHeight,
          minHeight: headHeight,
        }}>
          <Toolbar {...commonProps} style={{width: dividerPos}}/>
          <Timebar {...commonProps} height={headHeight}/>
        </div>
        <DividerLine ref={dragRef} position={dividerPos}/>
        <Scrollable
          style = {{display: 'flex', flex: 1, alignItems: 'flex-start', flexDirection: 'row-reverse'}}
          onChangeVerticalScroll = {this.handleChangeScrollPosition}
          verticalScroll = {scrollPosition}>
          <Keylines {...commonProps}/>
          <div style={{width: dividerPos}}>
            <Controls {...commonProps}/>
          </div>
        </Scrollable>
        <InlineEaseEditor {...{
            timeline,
            actions,
            dividerPos,
            scrollPosition,
          }}/>
      </div>
    </HotKeys>
  }
}
