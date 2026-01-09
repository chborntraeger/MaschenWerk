import { auth } from '@/auth';
import { createAuthenticatedClient } from '@/lib/directus';
import { deleteItem } from '@directus/sdk';
import { NextRequest, NextResponse } from 'next/server';

export async function DELETE(
  request: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  const session = await auth();
  const { id } = await params;

  if (!session?.user) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  // Check if user is admin
  if (session.user.role !== 'Administrator') {
    return NextResponse.json({ error: 'Forbidden' }, { status: 403 });
  }

  try {
    const { client } = createAuthenticatedClient(session.user.accessToken);
    
    await client.request(deleteItem('patterns', id));
    
    return NextResponse.json({ success: true });
  } catch (error) {
    console.error('Delete pattern error:', error);
    return NextResponse.json(
      { error: 'Failed to delete pattern' },
      { status: 500 }
    );
  }
}
