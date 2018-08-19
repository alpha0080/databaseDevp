import {defineModel, createModel, deserialise} from 'afflatus'
import {recurseKeys} from './recursers'

defineModel({
  type: 'State',
  simpleValues: {
    currentProject: {type: 'Project', canBeNull: true},
    // history: {type: 'History'},
  },
  arrayValues: {
    projects: {type: 'Project'},
  },
  computedValues: {
    currentTimeline() {
      return this.currentProject && this.currentProject.currentTimeline
    },
    currentTrack() {
      return this.currentTimeline && this.currentTimeline.currentTrack
    },
    selectedKeys() {
      const result = []
      recurseKeys(this.currentTimeline, key => {
        if (key.selected) {
          result.push(key)
        }
      })
      return result
    }
  },
  untrackedValues: {
    loadProject(source) {
      const project = deserialise(source)
      this.projects.push(project)
      return project
    },
    createNewProject() {
      const project = deserialise([
        {$id: 0, type: 'Project', name: 'new project', timelines: [1], currentTimeline: 1},
        {$id: 1, type: 'Timeline', name: 'new timeline'},
      ])
      project.currentTimeline.registerPreview(document.body, new TimelineMax())
      this.projects.push(project)
      return project
    }
  }
})

export default createModel('State')
