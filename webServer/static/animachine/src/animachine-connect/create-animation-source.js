import createEaser from './createEaser'
import createTargets from './createTargets'

function find (items, key, value) {
  for (let i = 0; i < items.length; ++i) {
    if (items[i][key] === value) {
      return items[i]
    }
  }
}

function uniq(items) {
  const result = []
  for (let i = 0; i < items.length; ++i) {
    if (result.indexOf(items[i]) === -1) {
      result.push(items[i])
    }
  }
  return result
}

function flatten(...items) {
  const result = []
  for (let i = 0; i < items.length; ++i) {
    result.push(...items[i])
  }
  return result
}

const sortKeys = (a, b) => a.time - b.time

const mergeTransformOriginParams = next => (params, targets, tlRoot) => {
  const transformOriginX = find(params, 'name', 'transformOriginX')
  const transformOriginY = find(params, 'name', 'transformOriginY')
  const transformOriginZ = find(params, 'name', 'transformOriginZ')

  if (transformOriginX || transformOriginY || transformOriginZ) {
    //remove all the transform origin params
    params = params.filter(({name}) => name.indexOf('transformOrigin') !== 0)
    const getKeys = param => param ? param.keys.map(key => key.time) : []
    const times = uniq(flatten(
      getKeys(transformOriginX),
      getKeys(transformOriginY),
      getKeys(transformOriginZ),
    ))

    let previousTransformOrigin = {x: 50, y: 50, z: 0}
    const getValue = (param, time, previousValue) => {
      const key = param && find(param.keys, 'time', time)
      return key ? key.value * 100 : previousValue
    }
    const keys = times.map(time => {
      const to = {
        x: getValue(transformOriginX, time, previousTransformOrigin.x),
        y: getValue(transformOriginY, time, previousTransformOrigin.y),
        z: getValue(transformOriginZ, time, previousTransformOrigin.z),
      }

      previousTransformOrigin = to

      return {time, value: `${to.x}% ${to.y}%`}
    })

    params = [...params, {name: 'transformOrigin', keys}]
  }

  next(params, targets, tlRoot)
}

const fixTransformOriginForSvgNodes = next => (params, targets, tlRoot) => {
  //TODO do this only if targets contains an svg
  const transformOriginParam = find(params, 'name', 'transformOrigin')
  if (!transformOriginParam || !find(transformOriginParam.keys, 'time', 0)) {
    tlRoot.set(targets, {transformOrigin: '50% 50%'}, 0)
  }

  next(params, targets, tlRoot)
}

const makeAllRotationShort = next => (params, targets, tlRoot) => {
  const rotationParams = [
    find(params, 'name', 'rotation'),
    find(params, 'name', 'rotationX'),
    find(params, 'name', 'rotationY'),
    find(params, 'name', 'rotationZ'),
  ].filter(param => !!param)

  rotationParams.forEach(param => {
    param.keys.forEach(key => key.value = `${key.value}_short`)
  })
  next(params, targets, tlRoot)
}


const addParamTimelines =
mergeTransformOriginParams(
fixTransformOriginForSvgNodes(
makeAllRotationShort(
  (params, targets, tlRoot) => {
    params.forEach(param => {
      const tlParam = new TimelineMax()
      tlRoot.add(tlParam, 0)
      let headTime = 0

      if (param.keys && param.keys.length) {
        const sortedKeys = param.keys.sort(sortKeys)

        //set the start position to the first key event is not in the time=0
        // so tartgets don't going to tween from they current position
        tlParam.set(targets, {[param.name]: sortedKeys[0].value})

        sortedKeys.forEach(key => {
          const duration = key.time - headTime

          tlParam.to(
            targets,
            duration / 1000,
            {
              [param.name]: key.value,
              smoothOrigin: false,//http://greensock.com/docs/#/HTML5/Plugins/CSSPlugin/
              ease: createEaser(key.ease)
            },
            headTime / 1000
          )
          headTime = key.time
        })
      }

      if (param.params) {
        addParams(param.params, targets)
      }
    })
  }
)))


export default function createAnimationSource(timeline, register) {
  function animationSource(rootTarget) {
    //to keep compatible with react-gsap-enhancer v0.2.x
    if (
      rootTarget.hasOwnProperty('target') &&
      rootTarget.hasOwnProperty('options')
    ) {
      rootTarget = rootTarget.target
    }
    //--------------------------------------------------

    const tlRoot = new TimelineMax()

    timeline.tracks.forEach(track => {
      const targets = track.selectors.map(selector => {
        return createTargets(rootTarget, selector)
      })

      addParamTimelines(track.params, targets, tlRoot)
    })

    //add to the animachine registry
    if (register) {
      register(rootTarget, tlRoot)
    }

    return tlRoot
  }

  return animationSource
}
