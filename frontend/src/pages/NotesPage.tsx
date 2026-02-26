import { useState } from 'react'
import { Plus, Search, Tag, Pin, Trash2, Edit } from 'lucide-react'
import { Sidebar } from '@/components/layout/Sidebar'
import { Header } from '@/components/layout/Header'
import { Card, CardContent } from '@/components/ui/Card'
import { Button } from '@/components/ui/Button'
import { Input } from '@/components/ui/Input'
import { Badge } from '@/components/ui/Badge'
import toast from 'react-hot-toast'

interface Note {
  id: string
  title: string
  content: string
  note_type: string
  tags: string[]
  is_pinned: boolean
  created_at: string
}

export function NotesPage() {
  const [searchQuery, setSearchQuery] = useState('')
  const [notes] = useState<Note[]>([]) // TODO: Load from API
  const [showNewNoteModal, setShowNewNoteModal] = useState(false)
  
  const filteredNotes = notes.filter(note =>
    note.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
    note.content.toLowerCase().includes(searchQuery.toLowerCase())
  )
  
  const pinnedNotes = filteredNotes.filter(n => n.is_pinned)
  const otherNotes = filteredNotes.filter(n => !n.is_pinned)
  
  return (
    <Sidebar>
      <Header />
      
      <div className="p-6">
        {/* Page Header */}
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-2xl font-bold text-dark-800">Notes</h1>
            <p className="text-dark-600 mt-1">Personal notes and meeting summaries</p>
          </div>
          
          <Button onClick={() => setShowNewNoteModal(true)}>
            <Plus className="h-5 w-5 mr-2" />
            New Note
          </Button>
        </div>
        
        {/* Search */}
        <Card className="mb-6">
          <CardContent className="py-4">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-dark-400" />
              <Input
                placeholder="Search notes..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="pl-10"
              />
            </div>
          </CardContent>
        </Card>
        
        {/* Pinned Notes */}
        {pinnedNotes.length > 0 && (
          <div className="mb-8">
            <h2 className="text-lg font-semibold text-dark-800 mb-4">Pinned</h2>
            <div className="grid gap-4">
              {pinnedNotes.map(note => (
                <NoteCard key={note.id} note={note} />
              ))}
            </div>
          </div>
        )}
        
        {/* All Notes */}
        {otherNotes.length > 0 || pinnedNotes.length === 0 ? (
          <div className="grid gap-4">
            {otherNotes.length > 0 && otherNotes.map(note => (
              <NoteCard key={note.id} note={note} />
            ))}
            
            {filteredNotes.length === 0 && (
              <Card>
                <CardContent className="py-12 text-center">
                  <p className="text-dark-600 mb-4">No notes yet</p>
                  <Button onClick={() => setShowNewNoteModal(true)}>
                    <Plus className="h-5 w-5 mr-2" />
                    Create Your First Note
                  </Button>
                </CardContent>
              </Card>
            )}
          </div>
        ) : null}
      </div>
      
      {/* New Note Modal */}
      {showNewNoteModal && <NewNoteModal onClose={() => setShowNewNoteModal(false)} />}
    </Sidebar>
  )
}

interface NoteCardProps {
  note: Note
}

function NoteCard({ note }: NoteCardProps) {
  return (
    <Card className="hover:shadow-md transition-shadow cursor-pointer">
      <CardContent className="py-4">
        <div className="flex items-start justify-between">
          <div className="flex-1">
            <div className="flex items-center space-x-2 mb-2">
              <h3 className="font-semibold text-dark-800">{note.title}</h3>
              {note.is_pinned && <Pin className="h-4 w-4 text-primary-600" />}
            </div>
            
            <p className="text-dark-600 text-sm mb-3 line-clamp-2">
              {note.content}
            </p>
            
            {note.tags.length > 0 && (
              <div className="flex flex-wrap gap-2">
                {note.tags.map((tag, i) => (
                  <Badge key={i} variant="info" size="sm">
                    <Tag className="h-3 w-3 mr-1" />
                    {tag}
                  </Badge>
                ))}
              </div>
            )}
          </div>
          
          <div className="flex items-center space-x-2">
            <Button variant="ghost" size="sm">
              <Edit className="h-4 w-4" />
            </Button>
            <Button variant="ghost" size="sm">
              <Trash2 className="h-4 w-4 text-red-600" />
            </Button>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}

interface NewNoteModalProps {
  onClose: () => void
}

function NewNoteModal({ onClose }: NewNoteModalProps) {
  const [title, setTitle] = useState('')
  const [content, setContent] = useState('')
  const [tags, setTags] = useState<string[]>([])
  const [tagInput, setTagInput] = useState('')
  
  const handleAddTag = () => {
    if (tagInput.trim() && !tags.includes(tagInput.trim())) {
      setTags([...tags, tagInput.trim()])
      setTagInput('')
    }
  }
  
  const handleSave = () => {
    if (!title.trim() || !content.trim()) {
      toast.error('Please fill in title and content')
      return
    }
    
    // TODO: Save to API
    toast.success('Note created!')
    onClose()
  }
  
  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <Card className="w-full max-w-2xl max-h-[80vh] overflow-y-auto">
        <CardContent className="py-6">
          <h2 className="text-lg font-semibold mb-4">Create New Note</h2>
          
          <div className="space-y-4">
            <Input
              label="Title"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="Note title"
            />
            
            <div>
              <label className="block text-sm font-medium text-dark-700 mb-1">
                Content
              </label>
              <textarea
                value={content}
                onChange={(e) => setContent(e.target.value)}
                placeholder="Write your note here..."
                className="w-full px-3 py-2 border border-dark-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 min-h-[200px]"
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-dark-700 mb-1">
                Tags
              </label>
              <div className="flex gap-2">
                <Input
                  value={tagInput}
                  onChange={(e) => setTagInput(e.target.value)}
                  onKeyDown={(e) => e.key === 'Enter' && (e.preventDefault(), handleAddTag())}
                  placeholder="Add a tag"
                  className="flex-1"
                />
                <Button type="button" onClick={handleAddTag} variant="outline">
                  Add
                </Button>
              </div>
              {tags.length > 0 && (
                <div className="flex flex-wrap gap-2 mt-2">
                  {tags.map((tag, i) => (
                    <Badge key={i} variant="info">
                      {tag}
                    </Badge>
                  ))}
                </div>
              )}
            </div>
          </div>
          
          <div className="flex justify-end space-x-3 mt-6">
            <Button variant="outline" onClick={onClose}>
              Cancel
            </Button>
            <Button onClick={handleSave}>
              Create Note
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
