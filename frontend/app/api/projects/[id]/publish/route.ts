import { auth } from '@/auth';
import { createAuthenticatedClient } from '@/lib/directus';
import { updateItem } from '@directus/sdk';
import { NextResponse } from 'next/server';

type RouteContext = {
  params: Promise<{ id: string }>;
};

export async function POST(request: Request, context: RouteContext) {
  try {
    const session = await auth();

    if (!session?.user) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    // Only admins can publish projects
    if (session.user.role !== 'Administrator') {
      return NextResponse.json({ error: 'Forbidden' }, { status: 403 });
    }

    const { id } = await context.params;

    // Use authenticated client
    const { client } = createAuthenticatedClient(session.user.accessToken!);

    // Update project status to public
    await client.request(
      updateItem('projects', id, {
        status: 'public',
      })
    );

    return NextResponse.json({ success: true });
  } catch (error) {
    console.error('Error publishing project:', error);
    return NextResponse.json({ error: 'Internal Server Error' }, { status: 500 });
  }
}
